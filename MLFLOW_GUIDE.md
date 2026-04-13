# 🧪 Guide Complet MLflow - Experiment Tracking

## 📋 Table des matières

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Structure MLflow](#structure)
4. [Utilisation complète](#utilisation)
5. [Intégration API](#api)
6. [Pipeline CI/CD](#cicd)
7. [Exemples pratiques](#exemples)
8. [Dépannage](#troubleshooting)

---

## 🎯 Introduction {#introduction}

**MLflow** est un outil pour tracker :
- ✅ **Paramètres** : hyperparamètres du modèle
- ✅ **Métriques** : performance (accuracy, loss, etc.)
- ✅ **Modèles** : sauvegarder les artifacts
- ✅ **Tags** : métadonnées sur les expériences
- ✅ **Prédictions** : résultats de test

```
Training → Metrics logged → MLflow UI → Visualiser & Comparer
```

---

## 📦 Installation {#installation}

### 1. MLflow est déjà dans `requirements.txt`

```bash
# Installer tout
pip install -r requirements.txt

# Ou seulement MLflow
pip install mlflow==2.14.1
```

### 2. Vérifier l'installation

```bash
# Voir la version
mlflow --version

# Ou dans Python
python -c "import mlflow; print(mlflow.__version__)"
```

---

## 🏗️ Structure MLflow {#structure}

### Dossiers créés

```
your_project/
├── mlruns/
│   ├── 0/              # Default experiment (ID: 0)
│   │   └── run_id_xxx/
│   │       ├── artifacts/
│   │       │   ├── model/
│   │       │   └── predictions.csv
│   │       ├── metrics/
│   │       ├── params/
│   │       └── tags
│   ├── 1/              # Movie Recommender Experiments (ID: 1)
│   │   ├── run_1/
│   │   ├── run_2/
│   │   └── run_3/
│   └── ...
```

---

## 🚀 Utilisation Complète {#utilisation}

### Option 1️⃣ : Script autonome

```bash
# Fichier déjà créé: train_and_track.py
python train_and_track.py
```

**Ce que ça fait :**
1. ✅ Charge les données
2. ✅ Construit les matrices
3. ✅ Lance l'expérience MLflow
4. ✅ Log paramètres, métriques, modèle
5. ✅ Sauvegarde predictions de test
6. ✅ Affiche résumé

**Output :**
```
🚀 MLflow Training & Tracking Pipeline
[1/5] 🎯 Initialisation de MLflow...
[2/5] 📂 Chargement des données...
  ✓ 9066 films chargés
  ✓ 100005 évaluations chargées
  ✓ 3683 tags chargés

[3/5] 🔨 Construction des matrices...
  ✓ Matrice utilisateur-film: (610, 9066)
  ✓ Matrice similarité genre construite

[4/5] ⚙️  Définition des hyperparamètres...
  • algorithm: hybrid
  • similarity_metric: cosine
  
[5/5] 📊 Tracking l'expérience...
📝 Logging des paramètres...
  ✓ algorithm: hybrid
  ✓ similarity_metric: cosine

🏷️  Logging des tags...
  ✓ model_type: hybrid
  ✓ version: v2.0

📊 Calcul des métriques...
  ✓ num_movies: 9066
  ✓ num_ratings: 100005
  ✓ avg_rating: 3.5256

✅ ENTRAÎNEMENT COMPLÉTÉ!
```

### Option 2️⃣ : Python interactif

```python
from ml_experiment_tracker import MLflowExperimentTracker
from ml_model import MovieRecommender

# Initialiser
tracker = MLflowExperimentTracker("My Experiment")

# Charger données
recommender = MovieRecommender().load_data()
recommender.build_user_item_matrix()
recommender.build_genre_similarity()

# Définir params
hyperparams = {
    "algorithm": "hybrid",
    "n_recommendations": 15
}

tags = {
    "version": "v2.1",
    "author": "Data Scientist"
}

# Tracker
metrics = tracker.track_training(recommender, hyperparams, tags)

# Logger predictions
predictions = recommender.get_recommendations_by_genres(1, n=10)
tracker.log_predictions(predictions, "test_output")
```

### Option 3️⃣ : MLflow API directly

```python
import mlflow

# Définir l'URI de tracking
mlflow.set_tracking_uri("./mlruns")

# Créer/récupérer une expérience
mlflow.set_experiment("My Experiment")

# Lancer un run
with mlflow.start_run():
    # Log paramètres
    mlflow.log_param("param1", value)
    
    # Log métriques
    mlflow.log_metric("accuracy", 0.95)
    
    # Log tags
    mlflow.set_tag("version", "v1.0")
    
    # Log artifacts
    mlflow.log_artifact("model.pkl")
    
    # Log modèle
    mlflow.sklearn.log_model(model, "model")
```

---

## 🔌 Intégration API Flask {#api}

### Routes disponibles

```
GET  /api/mlflow/status           → Statut global MLflow
POST /api/mlflow/train            → Déclencher training
GET  /api/mlflow/experiments      → Lister expériences
GET  /api/mlflow/runs/<exp_id>    → Lister runs d'une expérience
GET  /api/mlflow/ui               → URL MLflow UI
```

### 1. Ajouter à `app.py`

```python
# En haut
from mlflow_routes import setup_mlflow_routes

# Après création du recommender
recommender = MovieRecommender().load_data()...

# Setup les routes MLflow
setup_mlflow_routes(app, recommender)
```

### 2. Utiliser les routes

**Déclencher un training :**
```bash
curl -X POST http://localhost:5000/api/mlflow/train \
  -H "Content-Type: application/json" \
  -d '{
    "model_type": "hybrid",
    "version": "v2.1",
    "author": "API User"
  }'

# Response:
{
  "status": "training_started",
  "message": "Training déclenché en arrière-plan",
  "tracking_uri": "./mlruns"
}
```

**Voir le statut :**
```bash
curl http://localhost:5000/api/mlflow/status

# Response:
{
  "experiment_exists": true,
  "runs_count": 5,
  "training_status": {
    "running": false,
    "progress": 100,
    "message": "Idle"
  }
}
```

**Lister les expériences :**
```bash
curl http://localhost:5000/api/mlflow/experiments
```

---

## 🔄 Pipeline CI/CD {#cicd}

### Workflow automatique

Ajout dans `.github/workflows/backend-ci.yml` :

```yaml
- name: 🧪 MLflow Training
  if: github.ref == 'refs/heads/main'
  run: |
    pip install -r requirements.txt
    python train_and_track.py
    
- name: 📊 Upload MLflow artifacts
  uses: actions/upload-artifact@v3
  with:
    name: mlflow-runs
    path: mlruns/
```

---

## 📊 Exemples Pratiques {#exemples}

### Exemple 1: Comparer 2 modèles

```python
tracker = MLflowExperimentTracker("Model Comparison")

# Model 1: Collaborative filtering
metrics1 = tracker.track_training(
    recommender1,
    hyperparams={"algorithm": "collaborative"},
    tags={"version": "v1.0"}
)

# Model 2: Content-based
metrics2 = tracker.track_training(
    recommender2,
    hyperparams={"algorithm": "content_based"},
    tags={"version": "v2.0"}
)

# Comparer
tracker.compare_runs()
```

### Exemple 2: Hyperparam tuning

```python
tracker = MLflowExperimentTracker("Hyperparam Tuning")

for n_neighbors in [5, 10, 15, 20]:
    for metric in ["euclidean", "cosine"]:
        tracker.track_training(
            recommender,
            hyperparams={
                "n_neighbors": n_neighbors,
                "metric": metric
            },
            tags={"tune_target": "n_neighbors vs metric"}
        )

# MLflow UI montrera la meilleure combinaison
```

### Exemple 3: Trouver le meilleur run

```python
tracker = MLflowExperimentTracker("My Experiment")

# Tracker plusieurs runs...

# Récupérer le meilleur
best_run = tracker.get_best_run(metric_name="avg_rating")

print(f"Meilleur run: {best_run['run_id']}")
print(f"Score: {best_run['metrics.avg_rating']}")
```

---

## 🎯 Visualisation MLflow UI

### Lancer l'interface

```bash
mlflow ui
```

### Ouvrir dans le navigateur

```
http://localhost:5000
```

### Que voir ?

1. **Experiments** : Toutes tes expériences
2. **Runs** : Tous les runs d'une expérience
3. **Parameters** : Hyperparamètres utilisés
4. **Metrics** : Valeurs des métriques
5. **Tags** : Métadonnées
6. **Artifacts** : Fichiers loggés (modèles, images, etc.)

### Contrôler la UI

- **Filtrer** : Par tag, métrique, etc.
- **Comparer** : Sélectionner 2+ runs et voir différences
- **Exporter** : Télécharger les résultats

---

## 📋 Vérifier l'installation

```bash
# Script de vérification
python verify_mlflow_setup.py
```

**Output :**
```
🧪 VÉRIFICATION DE L'INTÉGRATION MLFLOW

📦 Test 1: Installation MLflow...
  ✅ MLflow 2.14.1 installé

📚 Test 2: Import du tracker...
  ✅ MLflowExperimentTracker importé

🎯 Test 3: Initialisation du tracker...
  ✅ Tracker initialisé

📁 Test 4: Répertoire mlruns...
  ✅ Répertoire ./mlruns créé

... (plus de tests)

📊 RÉSUMÉ DES TESTS
✅ Réussis: 9/10 (90%)

🎉 Tous les tests passés! MLflow est prêt!

🚀 Prochaines étapes:
   1. Exécuter: python train_and_track.py
   2. Visualiser: mlflow ui
   3. Ouvrir: http://localhost:5000
```

---

## 🐛 Dépannage {#troubleshooting}

### ❌ "ModuleNotFoundError: No module named 'mlflow'"

```bash
pip install mlflow
```

### ❌ "mlruns/ directory not found"

Pas de problème ! `mlruns/` est créé au premier run :

```bash
python train_and_track.py  # Crée mlruns/
```

### ❌ "Connection refused" au MLflow UI

```bash
# S'assurer que MLflow UI est lancé
mlflow ui

# Puis dans une autre console
# Ouvrir: http://localhost:5000
```

### ❌ "Failed to create experiment"

Peut-être que l'expérience existe déjà. C'est normal ! MLflow recréé automatiquement.

### ❌ "Metrics contains NaN or inf"

Le problème : division par zéro ou donnée invalide

Solution :
```python
# Dans _compute_metrics()
if total_cells > 0:
    metrics["sparsity"] = zero_count / total_cells
else:
    metrics["sparsity"] = 0  # Défaut
```

---

## 🔑 Bonnes pratiques

### ✅ À faire

| À faire |
|---------|
| Lancer training avec `python train_and_track.py` |
| Comparer runs dans MLflow UI |
| Logger les hyperparamètres significatifs |
| Utiliser des tags pour organiser |
| Sauvegarder les modèles pouvoir les réutiliser |
| Nettoyer `mlruns/` régulièrement si trop volumineux |

### ❌ À éviter

| À éviter |
|----------|
| Ne pas logger = pas de traçabilité |
| Hyperparamètres non documentés |
| Modèles sans version |
| Oublier le taggage (v1.0, v2.0, etc.) |
| Garder infiniment de runs (archiver régulièrement) |

---

## 📚 Ressources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MLflow API Reference](https://mlflow.org/docs/latest/python_api/index.html)
- [MLflow Models](https://mlflow.org/docs/latest/models.html)
- [Tracking API](https://mlflow.org/docs/latest/tracking.html)

---

## ✅ Quick Start

```bash
# 1. Vérifier
python verify_mlflow_setup.py

# 2. Lancer training
python train_and_track.py

# 3. Visualiser
mlflow ui

# 4. Ouvrir navigateur
# → http://localhost:5000
```

**🎉 Voilà ! Tu as maintenant un système complet de tracking ML ! 🚀**
