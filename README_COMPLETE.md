# 🎬 RecMovies - Movie Recommendation System

> **Système complet de recommandation de films avec ML, CI/CD, et tracking MLflow**

## 📋 Vue d'ensemble

RecMovies est une application **full-stack** de recommandation de films:

```
🎨 Frontend React/Vite     →    🔌 Backend Flask API    →    🗄️  PostgreSQL
     (Vercel)                      (Render)                    (Render)
     
     + MLflow Tracking (Experiments & Metrics)
     + GitHub Actions (CI/CD)
```

---

## 🚀 Quick Start

### Installation

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
cd ..
```

### Développement local

```bash
# 1. Backend
python app.py

# 2. Frontend (autre terminal)
cd frontend
npm run dev

# 3. MLflow (optionnel, autre terminal)
mlflow ui
```

### Production

- **Frontend** : Vercel
- **Backend** : Render
- **Database** : PostgreSQL sur Render

---

## 📁 Structure du projet

```
reco_movies/
├── app.py                          # Flask API principale
├── ml_model.py                     # Modèle ML recommendations
├── database.py                     # Models SQLAlchemy
├── seed.py                         # Données de test
├── requirements.txt                # Dépendances Python
│
├── 🧪 MLflow Integration
├── train_and_track.py              # Script training complet
├── ml_experiment_tracker.py        # Classe tracker MLflow
├── mlflow_routes.py                # Routes Flask/MLflow
├── verify_mlflow_setup.py          # Vérification setup
├── MLFLOW_GUIDE.md                 # Documentation MLflow
├── MLFLOW_SUMMARY.md               # Résumé MLflow
│
├── 🚀 CI/CD & Deployment
├── .github/workflows/
│   ├── backend-ci.yml              # Tests + Deploy Render
│   └── frontend-ci.yml             # Build + Deploy Vercel
├── render.yaml                     # Config Render
├── frontend/vercel.json            # Config Vercel
├── CI_CD_GUIDE.md                  # Guide CI/CD
├── DEPLOY_RENDER_VERCEL.md         # Guide déploiement
├── SETUP_GITHUB_SECRETS.md         # Setup secrets GitHub
│
├── 📊 Frontend
├── frontend/
│   ├── src/
│   │   ├── components/             # React components
│   │   ├── pages/                  # Pages
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── 📚 Data & Models
├── movies.csv
├── ratings.csv
├── tags.csv
├── links.csv
└── posters/                        # Cache posters TMDB
```

---

## 🎯 Guide par cas d'usage

### 1️⃣ Développement local

```bash
# Démarrer le backend
python app.py

# Démarrer le frontend
cd frontend && npm run dev

# Lancer MLflow (optionnel)
mlflow ui
```

**API disponible** : http://localhost:5000
**Frontend** : http://localhost:5173

---

### 2️⃣ MLflow - Experiment Tracking

```bash
# Vérifier setup MLflow
python verify_mlflow_setup.py

# Lancer le training complet
python train_and_track.py

# Visualiser les résultats
mlflow ui
# → http://localhost:5000
```

**Fichiers utiles** :
- [MLFLOW_GUIDE.md](MLFLOW_GUIDE.md) - Documentation complète
- [MLFLOW_SUMMARY.md](MLFLOW_SUMMARY.md) - Résumé rapide

---

### 3️⃣ CI/CD avec GitHub Actions

**Déploiement automatique :**

```bash
# Pusher sur main automatise:
# 1. Tests (pytest, ESLint)
# 2. Build (Vite, gunicorn)
# 3. Deploy (Vercel, Render)

git push origin main
```

**Fichiers utiles** :
- [CI_CD_GUIDE.md](CI_CD_GUIDE.md) - Guide complet
- Workflows : `.github/workflows/`

---

### 4️⃣ Déploiement Render + Vercel

**Setup** :

1. **Render** (Backend) :
   - Web Service : `gunicorn app:app`
   - PostgreSQL : Créer une instance

2. **Vercel** (Frontend) :
   - Framework : Vite
   - Root directory : `./frontend`

**Fichiers utiles** :
- [DEPLOY_RENDER_VERCEL.md](DEPLOY_RENDER_VERCEL.md) - Guide détaillé
- [SETUP_GITHUB_SECRETS.md](SETUP_GITHUB_SECRETS.md) - Configurer secrets

---

## 📖 Documentation

| Guide | Description |
|-------|-------------|
| [MLFLOW_GUIDE.md](MLFLOW_GUIDE.md) | 📊 Tracking expériences ML (complet) |
| [MLFLOW_SUMMARY.md](MLFLOW_SUMMARY.md) | 📊 Résumé MLflow (quick reference) |
| [CI_CD_GUIDE.md](CI_CD_GUIDE.md) | 🔄 Intégration continue (complet) |
| [DEPLOY_RENDER_VERCEL.md](DEPLOY_RENDER_VERCEL.md) | 🚀 Déployer Render/Vercel |
| [SETUP_GITHUB_SECRETS.md](SETUP_GITHUB_SECRETS.md) | 🔑 Configurer GitHub secrets |

---

## 🧪 Scripts disponibles

```bash
# Backend
python app.py                        # Lancer API
python seed.py                       # Charger données
python train_and_track.py            # Training MLflow
python verify_mlflow_setup.py        # Vérifier setup

# Frontend
cd frontend
npm run dev                          # Dev server
npm run build                        # Production build
npm run lint                         # Vérifier code
npm run preview                      # Preview build

# MLflow
mlflow ui                            # UI MLflow
```

---

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────────┐
│                    Utilisateurs                        │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
   🎨 Frontend              🌐 Backend
   (React/Vite)            (Flask API)
   (Vercel)                (Render)
        │                         │
        │    http/REST            │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │   🗄️ PostgreSQL         │
        │   (Render)              │
        └─────────────────────────┘

   + 🧪 MLflow (Tracking)
   + 🔄 GitHub Actions (CI/CD)
```

---

## 🔐 Authentification & Secrets

### Variables d'environnement requises

```bash
# .env
FLASK_ENV=development
DATABASE_URL=postgresql://user:pass@host/db
CORS_ORIGIN=http://localhost:5173
```

### GitHub Secrets

```
RENDER_SERVICE_ID           # ID service Render
RENDER_DEPLOY_KEY           # Clé API Render
VERCEL_TOKEN                # Token Vercel
VERCEL_ORG_ID               # Org ID Vercel
VERCEL_PROJECT_ID           # Project ID Vercel
```

---

## 📊 APIs disponibles

### Recommandations

```
POST /api/recommandations
Body: {"genres": ["Action", "Sci-Fi"], "n": 10}
```

### Top Films

```
GET /api/top-films?n=20&skip=0
```

### Genres

```
GET /api/genres
```

### MLflow (nouveau) 🆕

```
GET  /api/mlflow/status
POST /api/mlflow/train
GET  /api/mlflow/experiments
POST /api/mlflow/ui
```

---

## 🧪 Tests

```bash
# Backend
pytest test_ml_recommendations.py -v

# Frontend
cd frontend
npm test

# MLflow vérification
python verify_mlflow_setup.py
```

---

## 🔄 Workflow en production

```
Developer pushes code
        ↓
GitHub Actions Tests
        ↓
✅ If passed:
  • Build Frontend
  • Build Backend
  • Deploy sur Vercel (frontend)
  • Deploy sur Render (backend)
  ↓
Live! 🎉
```

---

## 📈 Monitoring

- **Render Dashboard** : Logs backend, metrics
- **Vercel Dashboard** : Performance frontend
- **MLflow UI** : Experiment tracking
- **GitHub Actions** : Workflow history

---

## 🐛 Troubleshooting

### Backend ne démarre pas

```bash
# Vérifier Python
python --version

# Vérifier dépendances
pip install -r requirements.txt

# Lancer avec debug
python app.py --debug
```

### Frontend ne build pas

```bash
# Vérifier Node
node --version

# Réinstaller deps
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### MLflow erreur

```bash
# Vérifier installation
python -c "import mlflow; print(mlflow.__version__)"

# Vérifier setup
python verify_mlflow_setup.py
```

### Déploiement échoue

- Vérifier logs GitHub Actions
- Vérifier secrets GitHub
- Vérifier Render/Vercel dashboards

---

## 📚 Ressources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [MLflow Documentation](https://mlflow.org/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)

---

## 👥 Contribution

1. Fork le repo
2. Créer une branche (`git checkout -b feature/amazing`)
3. Commit (`git commit -m "Add amazing feature"`)
4. Push (`git push origin feature/amazing`)
5. Open PR

---

## 📄 License

MIT License - Libre d'utilisation

---

## 🎉 Ready to go!

```bash
# Développement
python app.py          # Backend sur 5000
cd frontend && npm run dev  # Frontend sur 5173

# MLflow
python train_and_track.py
mlflow ui              # Visualiser sur 5000

# Production
git push origin main   # Déploie automatiquement!
```

**Questions ?** Consulte les guides dans [la documentation](#-documentation)

---

**🚀 Bon développement ! 🎬**
