"""
Script complet d'entraînement et tracking avec MLflow
Lance l'entraînement du modèle de recommandation et log tout dans MLflow
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent))

from ml_model import MovieRecommender
from ml_experiment_tracker import MLflowExperimentTracker
import mlflow


def main():
    """Fonction principale pour entraîner et tracker"""
    
    print("\n" + "="*60)
    print("🚀 MLflow Training & Tracking Pipeline")
    print("="*60)
    
    # 1️⃣  Initialiser MLflow
    print("\n[1/5] 🎯 Initialisation de MLflow...")
    tracker = MLflowExperimentTracker(
        experiment_name="Movie Recommender Experiments",
        tracking_uri="./mlruns"
    )
    
    try:
        # 2️⃣  Charger les données
        print("\n[2/5] 📂 Chargement des données...")
        recommender = MovieRecommender()
        recommender.load_data()
        print(f"  ✓ {len(recommender.movies)} films chargés")
        print(f"  ✓ {len(recommender.ratings)} évaluations chargées")
        print(f"  ✓ {len(recommender.tags)} tags chargés")
        
        # 3️⃣  Construire les matrices
        print("\n[3/5] 🔨 Construction des matrices...")
        recommender.build_user_item_matrix()
        print(f"  ✓ Matrice utilisateur-film: {recommender.user_item_matrix.shape}")
        
        recommender.build_genre_similarity()
        print(f"  ✓ Matrice similarité genre construite")
        
        # 4️⃣  Définir les paramètres
        print("\n[4/5] ⚙️  Définition des hyperparamètres...")
        hyperparams = {
            "algorithm": "hybrid",
            "similarity_metric": "cosine",
            "n_recommendations": 10,
            "max_depth": 5,
            "min_ratings": 3,
        }
        
        tags = {
            "model_type": "hybrid",
            "version": "v2.0",
            "dataset": "movielens-small",
            "author": "ML Team",
            "environment": "production" if os.getenv("FLASK_ENV") == "production" else "development"
        }
        
        for key, value in hyperparams.items():
            print(f"  • {key}: {value}")
        
        # 5️⃣  Tracker l'entraînement
        print("\n[5/5] 📊 Tracking l'expérience...")
        metrics = tracker.track_training(
            recommender=recommender,
            hyperparams=hyperparams,
            tags=tags,
            run_name=f"hybrid_model_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        # 6️⃣  Logger quelques prédictions de test
        print("\n[BONUS] 🧪 Logging des prédictions de test...")
        try:
            test_predictions = recommender.get_recommendations_by_genres(movie_id=1, n=10)
            if not test_predictions.empty:
                tracker.log_predictions(test_predictions, "test_genre_recommendations")
                print("  ✓ 10 recommandations loggées")
            
            test_predictions_rating = recommender.get_recommendations_by_ratings(user_id=1, n=10)
            if not test_predictions_rating.empty:
                tracker.log_predictions(test_predictions_rating, "test_rating_recommendations")
                print("  ✓ 10 recommandations par ratings loggées")
        except Exception as e:
            print(f"  ⚠️  Impossible de logger prédictions: {e}")
        
        # 7️⃣  Afficher résumé
        print("\n" + "="*60)
        print("✅ ENTRAÎNEMENT COMPLÉTÉ!")
        print("="*60)
        print(f"\n📊 Métriques calculées:")
        for metric, value in metrics.items():
            if isinstance(value, float):
                print(f"  • {metric}: {value:.4f}")
            else:
                print(f"  • {metric}: {value}")
        
        print(f"\n📁 Données sauvegardées dans: ./mlruns/")
        print(f"\n🎯 Pour visualiser les résultats:")
        print(f"   $ mlflow ui")
        print(f"   → Ouvre http://localhost:5000\n")
        
        # Comparer avec les autres runs
        print("\n📈 Historique des runs:")
        tracker.compare_runs()
        
        # Récupérer le meilleur run
        best_run = tracker.get_best_run(metric_name="avg_rating")
        if best_run is not None:
            print(f"\n🏆 Meilleur run trouvé avec avg_rating")
        
        return 0
    
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import pandas as pd
    exit_code = main()
    sys.exit(exit_code)
