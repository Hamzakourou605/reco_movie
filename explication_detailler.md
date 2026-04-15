# 🎬 RecMovies - Documentation Détaillée de l'Application

Ce document explique en détail le fonctionnement technique, l'architecture et les processus d'automatisation de l'application **RecMovies**.

---

## 1. 🏗️ Architecture Globale

L'application suit une architecture **full-stack** moderne et découplée :

### 🎨 Frontend (Interface Utilisateur)
- **Technologie** : React.js avec Vite.
- **Rôle** : Fournir une interface interactive pour rechercher des films, voir les tops et obtenir des recommandations.
- **Déploiement** : Hébergé sur **Vercel**.
- **Communication** : Requêtes REST vers l'API Backend.

### 🔌 Backend (API & Logique)
- **Technologie** : Flask (Python).
- **Rôle** : Gérer les routes API, interagir avec la base de données et piloter le moteur de Machine Learning.
- **Déploiement** : Hébergé sur **Render**.

### 🗄️ Base de Données
- **Technologie** : PostgreSQL.
- **Rôle** : Stocker les métadonnées des films, les évaluations (ratings) et les tags des utilisateurs.

---

## 🤖 2. Machine Learning (Moteur de Recommandation)

Le fichier `ml_model.py` contient la classe `MovieRecommender` qui utilise une approche **hybride** :

### A. Filtrage basé sur le contenu (Content-Based)
Il analyse les caractéristiques intrinsèques des films (genres, tags) :
- **Vectorisation** : Utilise `TfidfVectorizer` pour transformer le texte en données mathématiques.
- **Calcul** : Utilise la **Similarité Cosinus** pour trouver les films les plus proches d'un film donné ou d'un genre choisi.

### B. Filtrage Collaboratif (Collaborative Filtering)
Il analyse les comportements des utilisateurs :
- **Matrice Utilisateur-Film** : Une grille montrant quel utilisateur a donné quelle note à quel film.
- **Logique** : Si l'utilisateur A et l'utilisateur B aiment les mêmes films, le système recommandera à A les films que B a aimés mais que A n'a pas encore vus.

---

## 🧪 3. MLflow (Expérimentation & Tracking)

MLflow agit comme un système de gestion de laboratoire pour le Machine Learning :

- **Expériences** : Chaque entraînement est traqué avec `ml_experiment_tracker.py`.
- **Paramètres** : Enregistre les réglages du modèle (ex: nombre de voisins, algorithme).
- **Métriques** : Enregistre la performance (ex: précision, temps de calcul).
- **Artifacts** : Sauvegarde les fichiers générés (modèle `.pkl`, graphiques de performance).
- **Visualisation** : Interface accessible via `mlflow ui` sur le port 5000.

---

## 🔄 4. CI/CD (Automatisation)

Le projet utilise **GitHub Actions** pour assurer la qualité et le déploiement automatique.

### Phase d'Intégration Continue (CI)
À chaque "Push" sur GitHub, le fichier `.github/workflows/backend-ci.yml` et `frontend-ci.yml` s'exécutent :
1. **Linting** : Vérification du style de code (Flake8, Black, ESLint).
2. **Tests Unitaires** : Exécution de `pytest` pour vérifier que le moteur ML fonctionne toujours correctement.
3. **Sécurité** : Scan des vulnérabilités avec `bandit`.

### Phase de Déploiement Continu (CD)
Si les tests réussissent sur la branche `main` :
- **Render** reçoit un signal pour mettre à jour le backend.
- **Vercel** déploie automatiquement la nouvelle version du frontend.

---

## 🚀 5. Guide d'utilisation rapide

### Développement local
```bash
# Lancer le backend
python app.py

# Lancer le frontend
cd frontend && npm run dev

# Lancer MLflow
mlflow ui
```

### Entraîner et tracker un nouveau modèle
```bash
python train_and_track.py
```

---

## 📁 Structure des fichiers essentiels

| Fichier | Rôle |
| :--- | :--- |
| `app.py` | Serveur Flask principal et routes API. |
| `ml_model.py` | Algorithmes de recommandation (Hybride). |
| `ml_experiment_tracker.py` | Classe d'intégration avec MLflow. |
| `database.py` | Modèles de données SQLAlchemy. |
| `seed.py` | Script pour peupler la base de données initiale. |
| `.github/workflows/` | Configuration de l'automatisation CI/CD. |

---

*Document généré pour l'analyse technique du projet RecMovies.*
