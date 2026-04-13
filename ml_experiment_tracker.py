"""
Module MLflow pour tracker les expériences d'apprentissage automatique
Permet de logger les paramètres, métriques et modèles
"""

import mlflow
import mlflow.sklearn
import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path
import traceback

# Import conditionnel pour éviter erreurs si ml_model n'est pas disponible
try:
    from ml_model import MovieRecommender
except ImportError:
    MovieRecommender = None


class MLflowExperimentTracker:
    """Classe pour tracker les expériences ML avec MLflow"""
    
    def __init__(self, experiment_name="Movie Recommender", tracking_uri="./mlruns"):
        """Initialise MLflow avec le nom de l'expérience
        
        Args:
            experiment_name: Nom de l'expérience
            tracking_uri: Chemin où stocker les données MLflow
        """
        self.experiment_name = experiment_name
        self.tracking_uri = tracking_uri
        
        try:
            # Crée le dossier si n'existe pas
            Path(tracking_uri).mkdir(parents=True, exist_ok=True)
            
            # Configure le répertoire où MLflow sauvegarde les données
            mlflow.set_tracking_uri(f"file:{os.path.abspath(tracking_uri)}")
            
            # Crée ou récupère l'expérience
            existing_exp = mlflow.get_experiment_by_name(experiment_name)
            if not existing_exp:
                mlflow.create_experiment(experiment_name)
            mlflow.set_experiment(experiment_name)
            print(f"✅ Expérience '{experiment_name}' initialisée")
            print(f"📁 Tracking URI: {tracking_uri}")
        except Exception as e:
            print(f"⚠️  Erreur lors de l'initialisation MLflow: {e}")
            traceback.print_exc()
    
    def track_training(self, recommender=None, 
                       hyperparams: dict = None, 
                       tags: dict = None,
                       run_name: str = None):
        """
        Lance une nouvelle expérience et track l'entraînement du modèle
        
        Args:
            recommender: Instance de MovieRecommender (optionnel)
            hyperparams: Dict des paramètres (ex: {"n_neighbors": 10})
            tags: Dict des tags (ex: {"model_type": "collaborative"})
            run_name: Nom du run (auto-généré si None)
        
        Returns:
            dict: Les métriques calculées
        """
        hyperparams = hyperparams or {}
        tags = tags or {"model_type": "unknown"}
        run_name = run_name or f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            with mlflow.start_run(run_name=run_name):
                
                # LOG PARAMÈTRES
                print("\n📝 Logging des paramètres...")
                for key, value in hyperparams.items():
                    try:
                        mlflow.log_param(key, str(value))
                        print(f"  ✓ {key}: {value}")
                    except Exception as e:
                        print(f"  ⚠️  Erreur logging {key}: {e}")
                
                # LOG TAGS
                print("\n🏷️  Logging des tags...")
                try:
                    mlflow.set_tags(tags)
                    for key, value in tags.items():
                        print(f"  ✓ {key}: {value}")
                except Exception as e:
                    print(f"  ⚠️  Erreur logging tags: {e}")
                
                # CALCUL DES MÉTRIQUES
                print("\n📊 Calcul des métriques...")
                metrics = self._compute_metrics(recommender)
                
                for metric_name, metric_value in metrics.items():
                    try:
                        if isinstance(metric_value, (int, float)) and not pd.isna(metric_value):
                            mlflow.log_metric(metric_name, float(metric_value))
                            print(f"  ✓ {metric_name}: {metric_value:.4f}")
                    except Exception as e:
                        print(f"  ⚠️  Erreur logging {metric_name}: {e}")
                
                # LOG MODÈLE (si recommender existe)
                if recommender is not None:
                    try:
                        print("\n💾 Logging du modèle...")
                        mlflow.sklearn.log_model(
                            recommender,
                            "recommender_model"
                        )
                        print("  ✅ Modèle loggé")
                    except Exception as e:
                        print(f"  ⚠️  Erreur logging modèle (non-bloquant): {e}")
                
                # LOG FICHIER DE CONFIG
                try:
                    config_file = "mlflow_config.json"
                    config_data = {
                        "experiment_date": datetime.now().isoformat(),
                        "metrics": {k: float(v) if isinstance(v, (int, float)) else str(v) 
                                   for k, v in metrics.items()},
                        "hyperparams": hyperparams,
                        "tags": tags
                    }
                    with open(config_file, "w") as f:
                        json.dump(config_data, f, indent=4)
                    mlflow.log_artifact(config_file)
                    print("\n📄 Config loggée")
                    # Nettoyer après upload
                    if os.path.exists(config_file):
                        os.remove(config_file)
                except Exception as e:
                    print(f"  ⚠️  Erreur logging config: {e}")
                
                print("\n✅ Expérience complétée!")
                return metrics
        
        except Exception as e:
            print(f"\n❌ Erreur globale lors du tracking: {e}")
            traceback.print_exc()
            return {}
    
    def _compute_metrics(self, recommender=None) -> dict:
        """Calcule les métriques du modèle"""
        metrics = {
            "timestamp": datetime.now().timestamp(),
        }
        
        if recommender is None:
            print("  ℹ️  Pas de recommender fourni, métriques basiques seulement")
            return metrics
        
        try:
            # Statut de données
            if hasattr(recommender, 'movies') and recommender.movies is not None:
                metrics["num_movies"] = len(recommender.movies)
            
            if hasattr(recommender, 'ratings') and recommender.ratings is not None:
                metrics["num_ratings"] = len(recommender.ratings)
                avg_rating = recommender.ratings['rating'].mean()
                if not pd.isna(avg_rating):
                    metrics["avg_rating"] = float(avg_rating)
            
            if hasattr(recommender, 'tags') and recommender.tags is not None:
                metrics["num_tags"] = len(recommender.tags)
            
            # Statut de construction des modèles
            if hasattr(recommender, 'user_item_matrix') and recommender.user_item_matrix is not None:
                metrics["num_users"] = len(recommender.user_item_matrix.index)
                total_cells = recommender.user_item_matrix.shape[0] * recommender.user_item_matrix.shape[1]
                if total_cells > 0:
                    zero_count = int((recommender.user_item_matrix == 0).sum().sum())
                    metrics["matrix_sparsity"] = float(zero_count / total_cells)
            
            if hasattr(recommender, 'genre_similarity') and recommender.genre_similarity is not None:
                metrics["genre_similarity_computed"] = 1.0
        
        except Exception as e:
            print(f"  ⚠️  Erreur calcul métriques: {e}")
            traceback.print_exc()
        
        return metrics
    
    def log_predictions(self, predictions_df: pd.DataFrame, 
                       test_name: str = "test_predictions"):
        """Log un DataFrame de prédictions"""
        try:
            csv_file = f"{test_name}.csv"
            predictions_df.to_csv(csv_file, index=False)
            mlflow.log_artifact(csv_file)
            print(f"✅ Prédictions loggées: {csv_file}")
            # Nettoyer après upload
            if os.path.exists(csv_file):
                os.remove(csv_file)
        except Exception as e:
            print(f"❌ Erreur logging prédictions: {e}")
            traceback.print_exc()
    
    def compare_runs(self, experiment_id=None):
        """Affiche une comparaison des runs"""
        try:
            if experiment_id is None:
                exp = mlflow.get_experiment_by_name(self.experiment_name)
                if exp is None:
                    print("❌ Expérience non trouvée")
                    return
                experiment_id = exp.experiment_id
            
            runs = mlflow.search_runs(experiment_ids=[experiment_id])
            if runs.empty:
                print("ℹ️  Aucun run trouvé")
                return
            
            print("\n📊 Résumé des runs:")
            print(runs[['run_id', 'status', 'start_time']].to_string())
        except Exception as e:
            print(f"⚠️  Erreur comparaison runs: {e}")
            traceback.print_exc()
    
    def get_best_run(self, metric_name: str = "avg_rating"):
        """Récupère le meilleur run selon une métrique"""
        try:
            exp = mlflow.get_experiment_by_name(self.experiment_name)
            if exp is None:
                print("❌ Expérience non trouvée")
                return None
            
            runs = mlflow.search_runs(
                experiment_ids=[exp.experiment_id],
                order_by=[f"metrics.{metric_name} DESC"],
                max_results=1
            )
            
            if runs.empty:
                print("ℹ️  Aucun run trouvé")
                return None
            
            best_run = runs.iloc[0]
            print(f"\n🏆 Meilleur run: {best_run['run_id']}")
            return best_run
        
        except Exception as e:
            print(f"⚠️  Erreur recherche meilleur run: {e}")
            traceback.print_exc()
            return None


# ============================================
# EXEMPLES D'UTILISATION
# ============================================

if __name__ == "__main__":
    print("🚀 Exemple: Tracking d'une expérience ML\n")
    
    # 1️⃣  Initialiser MLflow
    tracker = MLflowExperimentTracker(experiment_name="Movie Recommender Experiments")
    
    if MovieRecommender is None:
        print("❌ ml_model non disponible. Installe les dépendances.")
        exit(1)
    
    # 2️⃣  Charger et traiter les données
    print("\n📂 Chargement du modèle...")
    try:
        recommender = MovieRecommender().load_data().build_user_item_matrix().build_genre_similarity()
    except Exception as e:
        print(f"❌ Erreur chargement: {e}")
        exit(1)
    
    # 3️⃣  Définir les paramètres
    hyperparams = {
        "algorithm": "hybrid",
        "similarity_metric": "cosine",
        "n_recommendations": 10
    }
    
    tags = {
        "model_type": "hybrid",
        "version": "v2.0",
        "author": "ML System"
    }
    
    # 4️⃣  Tracker l'entraînement
    metrics = tracker.track_training(recommender, hyperparams, tags)
    
    # 5️⃣  Logger des prédictions de test
    try:
        test_predictions = recommender.get_recommendations_by_genres(movie_id=1, n=10)
        if not test_predictions.empty:
            tracker.log_predictions(test_predictions, "genre_based_predictions")
    except Exception as e:
        print(f"⚠️  Erreur logging prédictions: {e}")
    
    print("\n🎉 Expérience complètement loggée dans MLflow!")
    print("   Exécute: mlflow ui")
    print("   Puis ouvre: http://localhost:5000")
