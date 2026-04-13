# 🚀 CI/CD Pipeline Guide

Ce projet inclut une **intégration continue et déploiement continu (CI/CD)** automatisée avec **GitHub Actions**.

## 📋 Table des matières

- [Comment ça fonctionne](#comment-ça-fonctionne)
- [Workflows disponibles](#workflows-disponibles)
- [Comment déclencher le CI/CD](#comment-déclencher-le-cicd)
- [Ajouter des secrets](#ajouter-des-secrets)
- [Dépannage](#dépannage)

---

## 🎯 Comment ça fonctionne

### Les 3 étapes du CI/CD

1. **✅ Test** → Exécute les tests automatiquement
2. **⚙️ Build** → Compile et construit le projet
3. **🚀 Deploy** → Déploie automatiquement sur main

```
git push sur branche main/develop
        ↓
GitHub Actions déclenche le workflow
        ↓
Tests lancés (Python + Frontend)
        ↓
Build si tests passent
        ↓
Déploiement (si main)
```

---

## 📁 Workflows disponibles

### 1️⃣ Backend CI/CD (`.github/workflows/backend-ci.yml`)

**Déclenché par :** Push sur `.py`, `requirements.txt`

**Actions :**
- ✅ Tests Python (pytest) sur 3 versions Python (3.9, 3.10, 3.11)
- 🎨 Lint (flake8, black, isort)
- 🔨 Build et vérification imports
- 🔐 Scan de sécurité (bandit, safety)

**Exemple de passage :**
```
✅ Tests Python & Lint ... PASSED
✅ Build Backend ... PASSED
✅ Sécurité & Dépendances ... PASSED
✅ Deploy Backend ... PASSED
```

### 2️⃣ Frontend CI/CD (`.github/workflows/frontend-ci.yml`)

**Déclenché par :** Push sur `frontend/**`

**Actions :**
- ✅ Tests React (npm test)
- 🎨 Lint (ESLint)
- 🔨 Build avec Vite
- 📊 Analyse de la taille du bundle
- 🔐 Audit des dépendances npm

**Exemple de passage :**
```
✅ Tests & Lint Frontend ... PASSED
✅ Performance & Bundle Size ... PASSED
✅ Sécurité Dependencies ... PASSED
```

---

## 🔄 Comment déclencher le CI/CD

### Automatiquement (recommandé)

```bash
# Sur branche develop (tests uniquement)
git push origin develop

# Sur branche main (tests + déploiement)
git push origin main
```

### Manuellement via GitHub

1. Va à **Actions** sur GitHub
2. Sélectionne le workflow
3. Clique sur **"Run workflow"**

---

## 🔑 Ajouter des secrets (pour déploiement)

Si tu veux déployer automatiquement (Vercel, AWS, etc.) :

1. Va sur **Settings** → **Secrets and variables** → **Actions**
2. Clique sur **"New repository secret"**
3. Ajoute tes secrets :

```
VERCEL_TOKEN=xxxxx       # Pour Vercel
HEROKU_API_KEY=xxxxx     # Pour Heroku
AWS_ACCESS_KEY_ID=xxxxx  # Pour AWS
```

### Utiliser un secret dans le workflow

```yaml
- name: Deploy to Vercel
  env:
    VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
  run: npm run deploy
```

---

## 📊 Surveiller les workflows

### Sur GitHub

1. Va à l'onglet **Actions**
2. Vois le statut de chaque workflow
3. Clique pour voir les détails et logs

### Status badge

Ajoute ceci dans ton `README.md` :

```markdown
![Backend CI/CD](https://github.com/[USER]/[REPO]/workflows/Backend%20CI%2FCD%20Pipeline/badge.svg)
![Frontend CI/CD](https://github.com/[USER]/[REPO]/workflows/Frontend%20CI%2FCD%20Pipeline/badge.svg)
```

---

## 🛠️ Configurer localement comme CI/CD

Pour tester avant de pusher :

```bash
# 1. Installer les dépendances dev
pip install -r requirements-dev.txt
cd frontend && npm install

# 2. Lancer les tests (backend)
pytest test_ml_recommendations.py -v

# 3. Lancer lint (backend)
flake8 . --max-line-length=127
black --check .
isort --check-only .

# 4. Tests & Build (frontend)
cd frontend
npm run lint
npm run build
```

---

## 🔐 Sécurité

### Backend

- **Bandit** : Scan les vulnérabilités de code Python
- **Safety** : Vérifie les dépendances Python dangereuses

### Frontend

- **npm audit** : Analyse les dépendances npm

### Pour voir les rapports

```bash
pip install bandit safety
bandit -r . -f txt
safety check
```

---

## 📝 Ajouter des étapes personnalisées

Exemple : Ajouter des tests supplémentaires

```yaml
- name: Tests MLflow
  run: |
    python -c "from ml_experiment_tracker import MLflowExperimentTracker; print('✅ MLflow OK')"
```

---

## 🚀 Déploiement automatique

### Exemple 1: Vercel (Frontend React)

```yaml
- name: Deploy to Vercel
  uses: vercel/actions/deploy@main
  env:
    VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
  with:
    deploy-args: "--prod"
```

### Exemple 2: Heroku (Backend Flask)

```yaml
- name: Deploy to Heroku
  run: |
    git remote add heroku https://git.heroku.com/[APP_NAME].git
    git push heroku main
  env:
    HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
```

### Exemple 3: AWS EC2

```yaml
- name: Deploy to AWS
  run: |
    mkdir -p ~/.ssh
    echo "${{ secrets.AWS_SSH_KEY }}" > ~/.ssh/id_rsa
    chmod 600 ~/.ssh/id_rsa
    ssh -i ~/.ssh/id_rsa ec2-user@${{ secrets.AWS_HOST }} 'cd app && git pull origin main && ./deploy.sh'
```

---

## ⚡ Optimisations

### Pour accélérer les builds

✅ **Cacheé les dépendances**
```yaml
cache: 'npm'  # Frontend
cache: 'pip'  # Backend
```

✅ **Parallelise les jobs**
```yaml
strategy:
  matrix:
    python-version: ["3.9", "3.10", "3.11"]
```

✅ **Conditions d'exécution**
```yaml
if: github.ref == 'refs/heads/main'  # Seulement sur main
```

---

## 🐛 Dépannage

### ❌ "Workflow failed: tests didn't pass"

```bash
# Teste localement d'abord
pytest test_ml_recommendations.py -v
npm test  # frontend
```

### ❌ "Permission denied" en déploiement

Ajoute ton SSH key dans les **Secrets** GitHub

### ❌ "Dépendances introuvables"

```bash
# Rafraîchis les caches
pip install --upgrade pip
npm install --legacy-peer-deps
```

---

## 📚 Ressources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)

---

## ✅ Checklist pour démarrer

- [ ] Pushes le code sur GitHub
- [ ] Va à **Settings** → **Actions** et **General**
- [ ] Active les workflows si désactivés
- [ ] Pousse sur `develop` pour tester
- [ ] Vérifie l'onglet **Actions** sur GitHub
- [ ] Ajoute les secrets si tu veux déployer
- [ ] Commande : `git push origin main` pour déployer

---

🎉 **Bravo ! Ton CI/CD est prêt !** 🚀
