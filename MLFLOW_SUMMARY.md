# 🧪 MLflow Integration Summary

## 📦 Fichiers ajoutés

| Fichier | Description | Rôle |
|---------|-------------|------|
| `train_and_track.py` | Script complet de training | **Lancer l'entraînement complet** |
| `ml_experiment_tracker.py` | Classe MLflow Tracker | **Logger les expériences** |
| `mlflow_routes.py` | Routes Flask pour MLflow | **API endpoints MLflow** |
| `verify_mlflow_setup.py` | Script de vérification | **Tester la configuration** |
| `MLFLOW_GUIDE.md` | Documentation complète | **Guide utilisateur** |
| `requirements.txt` | ✅ Mis à jour avec mlflow | **Dépendance MLflow** |

---

## 🚀 Quick Start

### 1️⃣ Installer

```bash
pip install -r requirements.txt
```

### 2️⃣ Vérifier

```bash
python verify_mlflow_setup.py
```

### 3️⃣ Lancer le training

```bash
python train_and_track.py
```

### 4️⃣ Visualiser

```bash
mlflow ui
# → Ouvre: http://localhost:5000
```

---

## 📋 Fichiers créés/modifiés

### Nouveaux fichiers

```
train_and_track.py                          → Script training complet
ml_experiment_tracker.py                    → Classe tracker (améliorée)
mlflow_routes.py                            → Routes Flask MLflow
verify_mlflow_setup.py                      → Vérification setup
MLFLOW_GUIDE.md                             → Documentation
MLFLOW_SUMMARY.md                           → Ce fichier
```

### Fichiers modifiés

```
requirements.txt                            → ✅ +mlflow==2.14.1
ml_experiment_tracker.py                    → 🔧 Gestion d'erreurs améliorée
```

---

## 🎯 Ce que MLflow track

```
✅ Paramètres         {"algorithm": "hybrid", "n_recommendations": 10}
✅ Métriques          {"num_movies": 9066, "avg_rating": 3.5256}
✅ Tags               {"version": "v2.0", "author": "ML Team"}
✅ Modèles            Sauvegarde complète du MovieRecommender
✅ Artifacts          Fichiers CSV de prédictions de test
✅ Configs            JSON avec l'historique
```

---

## 🔄 Intégration avec l'API Flask

Pour ajouter les endpoints MLflow à ton app Flask :

```python
# app.py
from mlflow_routes import setup_mlflow_routes

# Après avoir créé le recommender
recommender = MovieRecommender().load_data()...

# Setup les routes
setup_mlflow_routes(app, recommender)
```

### Routes disponibles

```
GET  /api/mlflow/status           → Statut MLflow + dernière expérience
POST /api/mlflow/train            → Déclencher training async
GET  /api/mlflow/experiments      → Lister toutes expériences
GET  /api/mlflow/runs/<exp_id>    → Lister runs d'une expérience
GET  /api/mlflow/ui               → Info pour accéder à MLflow UI
```

---

## 📊 Structure MLflow

```
mlruns/
├── 0/                    # Expérience default
├── 1/                    # Movie Recommender Experiments
│   ├── run_1/
│   │   ├── artifacts/
│   │   │   ├── model/                    → Modèle sauvegardé
│   │   │   ├── genre_based_predictions.csv
│   │   │   └── mlflow_config.json
│   │   ├── metrics/
│   │   │   ├── num_movies
│   │   │   ├── avg_rating
│   │   │   └── matrix_sparsity
│   │   ├── params/
│   │   │   ├── algorithm
│   │   │   ├── similarity_metric
│   │   │   └── n_recommendations
│   │   └── tags
│   │       ├── model_type: hybrid
│   │       ├── version: v2.0
│   │       └── author: ML Team
│   ├── run_2/
│   └── run_3/
└── ...
```

---

## 🧪 Exemples d'utilisation

### Exemple 1: Simple

```python
from ml_experiment_tracker import MLflowExperimentTracker
from ml_model import MovieRecommender

tracker = MLflowExperimentTracker()
recommender = MovieRecommender().load_data()

metrics = tracker.track_training(
    recommender,
    {"algorithm": "hybrid"},
    {"version": "v2.0"}
)
```

### Exemple 2: Script automatisé

```bash
python train_and_track.py
```

### Exemple 3: Via l'API

```bash
curl -X POST http://localhost:5000/api/mlflow/train \
  -H "Content-Type: application/json" \
  -d '{
    "model_type": "hybrid",
    "version": "v2.1",
    "author": "API User"
  }'
```

### Exemple 4: Dans le code

```python
# Direct MLflow API
import mlflow

mlflow.set_experiment("My Experiment")

with mlflow.start_run():
    mlflow.log_param("param1", value1)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.set_tag("version", "v1.0")
```

---

## 📈 Visualisation

### MLflow UI

```bash
mlflow ui
# → http://localhost:5000
```

**Features :**
- 📊 Voir tous les runs
- 🔄 Comparer les runs
- 📈 Graphiques des métriques
- 🏆 Meilleur run
- 📥 Télécharger les données
- 🏷️ Filtrer par tags

---

## 🔐 CI/CD Integration

Les workflows GitHub Actions peuvent tracker automatiquement :

```yaml
- name: 🧪 MLflow Training
  run: |
    pip install -r requirements.txt
    python train_and_track.py

- name: 📊 Upload artifacts
  uses: actions/upload-artifact@v3
  with:
    name: mlflow-runs
    path: mlruns/
```

---

## ✅ Vérification

### Test complet

```bash
python verify_mlflow_setup.py
```

**Output :**
```
🧪 VÉRIFICATION DE L'INTÉGRATION MLFLOW
✅ Test 1: Installation MLflow... PASSED
✅ Test 2: Import du tracker... PASSED
✅ Test 3: Initialisation tracker... PASSED
✅ Test 4: Répertoire mlruns... PASSED
✅ Test 5: Script training... PASSED
... (plus de tests)

📊 RÉSUMÉ DES TESTS
✅ Réussis: 10/10 (100%)

🎉 Tous les tests passés!
```

---

## 🐛 Troubleshooting

### ❌ ModuleNotFoundError: mlflow

```bash
pip install mlflow
```

### ❌ mlruns/ doesn't exist

C'est normal ! Créé au premier run :

```bash
python train_and_track.py
```

### ❌ MLflow UI not connecting

```bash
# S'assurer que mlflow ui est lancé
mlflow ui

# Puis ouvrir dans une autre fenêtre
http://localhost:5000
```

### ❌ "Failed to create experiment"

Pas de problème, l'expérience existe probablement déjà. MLflow recréé automatiquement.

---

## 🎓 Prochaines étapes

1. **✅ Tester localement** : `python train_and_track.py`
2. **✅ Visualiser** : `mlflow ui`
3. **✅ Comparer runs** : Dans l'UI, sélectionner plusieurs runs
4. **✅ Intégrer à l'API** : Ajouter à `app.py`
5. **✅ Automatiser en CI/CD** : Ajouter à `.github/workflows/`

---

## 📚 Documentation

- [MLFLOW_GUIDE.md](MLFLOW_GUIDE.md) - Guide complet
- [MLflow Official Docs](https://mlflow.org/docs/latest/index.html)
- [train_and_track.py](train_and_track.py) - Exemple complet

---

## 🎉 Bravo !

MLflow est maintenant complètement intégré au projet !

```
Training Script  → train_and_track.py
        ↓
Track Metrics    → ml_experiment_tracker.py
        ↓
Log Artifacts    → mlruns/
        ↓
Visualize        → mlflow ui
        ↓
Compare Runs     → MLflow UI
```

**🚀 Prêt à tracker tes expériences !**
