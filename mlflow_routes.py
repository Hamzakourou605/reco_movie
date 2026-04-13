"""
Routes Flask pour intégration MLflow
À ajouter dans app.py après les autres imports
"""

from flask import jsonify, request
import threading
from ml_experiment_tracker import MLflowExperimentTracker
from ml_model import MovieRecommender
import mlflow

# État du training
training_status = {
    "running": False,
    "progress": 0,
    "message": "Idle",
    "last_run": None,
    "error": None
}


def setup_mlflow_routes(app, recommender):
    """
    Configure les routes MLflow sur l'application Flask
    
    Args:
        app: L'instance Flask
        recommender: L'instance du MovieRecommender
    """
    
    @app.route("/api/mlflow/status", methods=["GET"])
    def mlflow_status():
        """Retourne le statut du training"""
        try:
            import mlflow
            exp = mlflow.get_experiment_by_name("Movie Recommender Experiments")
            
            if exp is None:
                return jsonify({
                    "experiment_exists": False,
                    "runs_count": 0,
                    "tracking_uri": mlflow.get_tracking_uri()
                })
            
            # Chercher les runs
            runs = mlflow.search_runs(experiment_ids=[exp.experiment_id])
            
            return jsonify({
                "experiment_exists": True,
                "experiment_id": exp.experiment_id,
                "runs_count": len(runs),
                "tracking_uri": mlflow.get_tracking_uri(),
                "training_status": training_status,
                "last_run": training_status["last_run"]
            })
        except Exception as e:
            return jsonify({
                "error": str(e),
                "tracking_uri": "Not configured"
            }), 500
    
    
    @app.route("/api/mlflow/train", methods=["POST"])
    def trigger_training():
        """
        Déclenche un training asynchrone et le track avec MLflow
        
        Body (optionnel):
        {
            "model_type": "hybrid",
            "version": "v2.0",
            "author": "API",
            "description": "Trained via API"
        }
        """
        
        if training_status["running"]:
            return jsonify({
                "error": "Training déjà en cours",
                "message": training_status["message"]
            }), 409
        
        def train_async():
            """Fonction de training asynchrone"""
            try:
                training_status["running"] = True
                training_status["message"] = "Initialisation..."
                training_status["error"] = None
                
                # Récupérer les paramètres
                data = request.get_json() or {}
                model_type = data.get("model_type", "hybrid")
                version = data.get("version", "v2.0")
                author = data.get("author", "API")
                description = data.get("description", "")
                
                print(f"\n🚀 Training déclenché via API")
                print(f"   Type: {model_type}")
                print(f"   Author: {author}")
                
                # Initialiser le tracker
                training_status["message"] = "Initialisation MLflow..."
                tracker = MLflowExperimentTracker(
                    experiment_name="Movie Recommender Experiments",
                    tracking_uri="./mlruns"
                )
                
                # Préparer l'expérience
                training_status["message"] = "Préparation des données..."
                hyperparams = {
                    "algorithm": "hybrid",
                    "similarity_metric": "cosine",
                    "n_recommendations": 10,
                    "model_type": model_type,
                }
                
                tags = {
                    "model_type": model_type,
                    "version": version,
                    "author": author,
                    "source": "API",
                    "description": description,
                }
                
                # Lancer le training
                training_status["message"] = "Training en cours..."
                training_status["progress"] = 50
                
                metrics = tracker.track_training(
                    recommender=recommender,
                    hyperparams=hyperparams,
                    tags=tags,
                    run_name=f"api_train_{model_type}"
                )
                
                training_status["progress"] = 90
                training_status["message"] = "Finalization..."
                
                # Logger les prédictions de test
                try:
                    test_predictions = recommender.get_recommendations_by_genres(
                        movie_id=1, n=10
                    )
                    if not test_predictions.empty:
                        tracker.log_predictions(test_predictions, "api_test_predictions")
                except:
                    pass
                
                training_status["message"] = "Terminé!"
                training_status["progress"] = 100
                training_status["last_run"] = {
                    "timestamp": str(__import__('datetime').datetime.now()),
                    "metrics": {k: float(v) if isinstance(v, (int, float)) else str(v) 
                               for k, v in metrics.items()},
                    "tags": tags
                }
                
            except Exception as e:
                print(f"❌ Erreur training: {e}")
                training_status["error"] = str(e)
                training_status["message"] = f"Erreur: {e}"
            
            finally:
                training_status["running"] = False
        
        # Lancer le training en thread asynchrone
        thread = threading.Thread(target=train_async, daemon=True)
        thread.start()
        
        return jsonify({
            "status": "training_started",
            "message": "Training déclenché en arrière-plan",
            "tracking_uri": "./mlruns"
        }), 202
    
    
    @app.route("/api/mlflow/experiments", methods=["GET"])
    def get_experiments():
        """Liste toutes les expériences MLflow"""
        try:
            experiments = mlflow.search_experiments()
            
            result = []
            for exp in experiments:
                runs = mlflow.search_runs(experiment_ids=[exp.experiment_id])
                result.append({
                    "experiment_id": exp.experiment_id,
                    "name": exp.name,
                    "runs_count": len(runs),
                    "creation_time": exp.creation_time,
                    "last_update": runs.iloc[0]["end_time"] if len(runs) > 0 else None
                })
            
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    
    @app.route("/api/mlflow/runs/<experiment_id>", methods=["GET"])
    def get_runs(experiment_id):
        """Liste tous les runs d'une expérience"""
        try:
            runs = mlflow.search_runs(experiment_ids=[experiment_id])
            
            result = []
            for _, run in runs.iterrows():
                result.append({
                    "run_id": run["run_id"],
                    "status": run["status"],
                    "start_time": str(run["start_time"]),
                    "end_time": str(run["end_time"]),
                    "metrics": {k.replace("metrics.", ""): v 
                               for k, v in run.items() 
                               if k.startswith("metrics.")},
                    "params": {k.replace("params.", ""): v 
                              for k, v in run.items() 
                              if k.startswith("params.")}
                })
            
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    
    @app.route("/api/mlflow/ui", methods=["GET"])
    def mlflow_ui_link():
        """Retourne l'URL de l'interface MLflow"""
        return jsonify({
            "ui_url": "http://localhost:5000",
            "instruction": "Assurez-vous que MLflow UI est lancé avec: mlflow ui",
            "mlruns_path": "./mlruns"
        })


# ============================================
# UTILISATION
# ============================================

"""
Pour utiliser ces routes dans app.py, ajoute après l'initialisation :

from mlflow_routes import setup_mlflow_routes

# ... code app.py ...

if __name__ == '__main__':
    # Charger le recommender
    recommender = MovieRecommender().load_data()...
    
    # Setup routes
    setup_mlflow_routes(app, recommender)
    
    # Lancer
    app.run(debug=False)
"""
