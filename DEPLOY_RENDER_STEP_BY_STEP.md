# 🚀 Guide Complet: Déployer sur Render

> Déploie ton backend Flask sur Render en 15 minutes

## 📋 Table des matières

1. [Prérequis](#prérequis)
2. [Étape 1: Créer compte Render](#étape-1-créer-compte-render)
3. [Étape 2: Configurer le backend](#étape-2-configurer-le-backend)
4. [Étape 3: Créer la base de données PostgreSQL](#étape-3-postgresql)
5. [Étape 4: Déployer](#étape-4-déployer)
6. [Étape 5: Vérifier](#étape-5-vérifier)
7. [Dépannage](#dépannage)

---

## ✅ Prérequis {#prérequis}

- ✅ Compte GitHub (avec le repo pushé)
- ✅ Fichiers essentiels dans le projet :
  - `app.py`
  - `requirements.txt`
  - `render.yaml` ✅ (déjà créé)
- ✅ `requirements.txt` mis à jour avec `gunicorn`

### Vérifier requirements.txt

```bash
# Le fichier doit contenir
gunicorn==21.2.0
Flask==3.0.0
Flask-Cors==4.0.0
# ... autres dépendances
```

---

## 🎯 Étape 1: Créer compte Render {#étape-1-créer-compte-render}

### 1️⃣ Va sur Render

```
https://render.com
```

### 2️⃣ Clique sur "Sign up"

![Sign up Render]

### 3️⃣ Choisir "Sign up with GitHub"

- Clique sur le bouton GitHub
- Autorise Render à accéder à tes repos
- Valide

### 4️⃣ Dashboard Render

Après connexion, tu vois :
```
┌─────────────────────────┐
│  Dashboard Render       │
├─────────────────────────┤
│ New +                   │ ← Clique ici
│                         │
│ Recent Services:        │
│ (vide pour l'instant)   │
└─────────────────────────┘
```

---

## ⚙️ Étape 2: Configurer le backend {#étape-2-configurer-le-backend}

### A) S'assurer que `render.yaml` existe

Le fichier est déjà créé ! Vérifie le contenu :

```bash
cat render.yaml
```

Il doit contenir :
```yaml
runtime: python-3.11
services:
  - type: web
    name: reco-movies-backend
    env: python
    plan: free
    branch: main
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn app:app --bind 0.0.0.0:$PORT"
    envVars:
      - key: FLASK_ENV
        value: production
```

### B) Créer Web Service sur Render

1. Dashboard Render → **New +** → **Web Service**

2. **Import from GitHub**
   - Cherche ton repo: `reco_movie`
   - Clique **Select**

3. **Configure Service**
   ```
   Name: reco-movies-backend
   Region: Singapore (ou plus proche)
   Branch: main
   Runtime: Python 3.11
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
   Plan: Free (gratuit avec limitation)
   ```

4. **Advanced Settings**
   - Scroll down
   - Add Environment Variable:
     ```
     FLASK_ENV = production
     ```

5. **Create Web Service**

### ⏳ Attends le build

```
Building...
Installation des dépendances
Setup app
Deploy en cours...
```

**C'est environ 5-10 minutes**

---

## 🗄️ Étape 3: PostgreSQL {#étape-3-postgresql}

### A) Créer base de données PostSQL

1. Dashboard Render → **New +** → **PostgreSQL**

2. **Configure Database**
   ```
   Database Name: reco_movies
   User: postgres
   Region: Singapore (même que backend)
   Plan: Free
   ```

3. **Create Database**

### B) Récupérer la connection string

Après création, tu vois :

```
Internal Database URL:
postgresql://user:password@dpg-xxxxx.internal/reco_movies

External Database URL:
postgresql://user:password@dpg-xxxxx.onrender.com/reco_movies
```

### C) Ajouter la DATABASE_URL au backend

1. Va à **Web Service** → **reco-movies-backend**
2. Clique sur **Environment**
3. Add Environment Variable:
   ```
   DATABASE_URL = [Copie l'External URL]
   ```
4. **Save**

### D) Redémarrer le service

1. Va à **Web Service**
2. Clique **Manual Deploy** → **Deploy latest commit**

---

## 🚀 Étape 4: Déployer {#étape-4-déployer}

### Option 1: Via Render Dashboard (Manuel)

1. Web Service → **Manual Deploy** → **Deploy latest commit**

### Option 2: Via GitHub (Automatique) 🔄

1. Pousse un commit
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. Render détecte et déploie automatiquement

---

## ✅ Étape 5: Vérifier {#étape-5-vérifier}

### A) Vérifier le statut

1. Web Service → **Logs**
2. Attends que ça dise: **"Server running"** ou **"listening on"**

### B) Récupérer l'URL

```
Web Service page
→ Voir le lien en haut:

https://reco-movies-backend-xxxxx.onrender.com
```

### C) Tester l'API

```bash
# Teste la health check
curl https://reco-movies-backend-xxxxx.onrender.com/health

# Réponse attendue:
{"status":"healthy","poster_cache_size":0}
```

### D) Tester une requête

```bash
curl https://reco-movies-backend-xxxxx.onrender.com/api/genres

# Réponse attendue:
["Action", "Adventure", "Animation", ...]
```

---

## 📋 Récapitulatif URLs

```
Backend: https://reco-movies-backend-xxxxx.onrender.com
Database: postgresql://user:pass@dpg-xxxxx.onrender.com/reco_movies
```

---

## 🐛 Dépannage {#dépannage}

### ❌ "Build failed"

**Problème:** Dépendances manquantes

**Solution:**
```bash
# Vérifier requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git push origin main
# Render redéploie
```

### ❌ "Service crashed"

**Problème:** Erreur dans app.py

**Vérifier:**
1. Va à **Logs**
2. Cherche l'erreur
3. Corrige dans `app.py`
4. Pousse: `git push origin main`

### ❌ "Database connection refused"

**Problème:** DATABASE_URL incorrect

**Solution:**
1. Web Service → **Environment**
2. Vérifier la `DATABASE_URL`
3. Assure-toi c'est l'**External URL**
4. Clique **Save**

### ❌ "Port already in use"

**Problème:** Conflit de port

**Solution:** Render gère les ports, pas ta responsabilité
- Assure-toi: `--bind 0.0.0.0:$PORT`

### ❌ "503 Service Unavailable"

**Problème:** Service pas encore prêt

**Solution:**
- Attends 1-2 min
- Rafraîchis la page
- Vérifier les logs

---

## 🔐 Variables d'environnement importantes

À ajouter dans **Environment** :

```
FLASK_ENV = production
DATABASE_URL = postgresql://...
CORS_ORIGIN = https://frontend-url.vercel.app
```

---

## 📊 Monitoring

### Voir les logs

```
Web Service → Logs
```

Cherche :
- ✅ "Server running"
- ❌ "Error" ou "Exception"

### Voir les métriques

```
Web Service → Metrics
```

- CPU usage
- Memory
- Requests

---

## 🎯 Prochaines étapes

1. ✅ Backend déployé sur Render
2. 🎨 Déployer frontend sur Vercel (cf. guide séparé)
3. 🔗 Connecter frontend ↔ backend
4. 🔄 Automatiser CI/CD (cf. CI_CD_GUIDE.md)

---

## 💡 Tips & Tricks

### Redéployer manuellement

```
Web Service page → Manual Deploy → Deploy latest commit
```

### Voir l'historique des déploiements

```
Web Service → Deployments
```

### Voir les fichiers du code

```
Web Service → Code
(lire-seul)
```

### SSH dans le service (advanced)

Render offre SSH pour debug avancé
```
Web Service → Shell
```

---

## 📚 Ressources

- [Render Docs](https://render.com/docs)
- [Render + Flask](https://render.com/docs/deploy-flask)
- [Render + PostgreSQL](https://render.com/docs/databases)

---

## ✅ Checklist finale

- [ ] Compte Render créé
- [ ] Web Service créé
- [ ] PostgreSQL créé
- [ ] DATABASE_URL configurée
- [ ] Build réussi (vert ✅)
- [ ] API répond à /health
- [ ] URL backend notée

```
https://reco-movies-backend-xxxxx.onrender.com
```

---

**🎉 Bravo ! Ton backend est live sur Render !** 🚀

Prochaine étape : [Déployer le frontend sur Vercel](DEPLOY_RENDER_VERCEL.md)
