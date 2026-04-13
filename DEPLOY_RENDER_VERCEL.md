# 🚀 Guide Déploiement - Render & Vercel

## 📋 Sommaire
1. [Déploiement Backend sur Render](#backend-render)
2. [Déploiement Frontend sur Vercel](#frontend-vercel)
3. [Architecture recommandée](#architecture)
4. [Variables d'environnement](#secrets)
5. [Dépannage](#troubleshooting)

---

## 🎯 Chose 1: Backend sur Render {#backend-render}

### Étape 1.1: Créer un compte Render
1. Va sur https://render.com
2. Clique **"Sign up with GitHub"**
3. Autorise l'accès à tes repos

### Étape 1.2: Créer le service Backend

**A. Nouvelle Web Service**
1. Dashboard Render → **"New +"** → **"Web Service"**
2. Sélectionne ton repo GitHub
3. Configure :

```
Name: reco-movies-backend
Branch: main
Runtime: Python 3.11
Build command: pip install -r requirements.txt
Start command: gunicorn app:app --bind 0.0.0.0:$PORT
Plan: Free (or Starter si tu veux plus stable)
```

**B. Variables d'environnement**

Va à **Settings** → **Environment** et ajoute :

```
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@host/reco_movies
CORS_ORIGIN=https://[ton-frontend-vercel].vercel.app
TMDB_API_KEY=e5c934fe24429749beb4d1f4724bb2ee
```

**C. Clique Deploy**

**D. Attends que ça build** (~5-10 min)

✅ Ton backend sera live à : `https://reco-movies-backend.onrender.com`

---

### Étape 1.3: Configurer la base de données PostgreSQL sur Render

1. Dashboard → **"New +"** → **"PostgreSQL"**
2. Configure :

```
Name: reco-movies-postgres
Plan: Free (avec limite)
  ou Starter (5$ presqu'gratuit)
```

3. Suite de la config :
   - Database: `reco_movies`
   - User: `postgres`
   - Password: **COPIE-LA !!**

4. JSON de connexion ressemble à :
```
postgresql://user:PASSWORD@host:5432/reco_movies
```

5. Ajoute l'URL dans le backend (variable `DATABASE_URL`)

---

## 🎨 Étape 2: Frontend sur Vercel {#frontend-vercel}

### Étape 2.1: Créer un compte Vercel

1. Va sur https://vercel.com
2. Clique **"Sign up with GitHub"**
3. Autorise l'accès

### Étape 2.2: Déployer le Frontend

**A. Import du projet**
1. Dashboard Vercel → **"Add New ..."** → **"Project"**
2. Sélectionne ton repo GitHub
3. Configure :

```
Framework Preset: Vite
Root Directory: ./frontend
Build Command: npm run build
Output Directory: dist
Remember: Leave empty if it auto-detects
```

**B. Variables d'environnement**

Clique **"Environment Variables"** et ajoute :

```
VITE_API_URL=https://reco-movies-backend.onrender.com
VITE_APP_NAME=MyTflix
```

**C. Deploy**

Clique **"Deploy"** → Attends (~3-5 min)

✅ Ton frontend sera live à : `https://[ton-projet].vercel.app`

---

## 🏗️ Architecture Recommandée {#architecture}

```
┌─────────────────────┐
│   Vercel Frontend   │  https://reco-movies.vercel.app
│   (React + Vite)    │
└──────────┬──────────┘
           │ CORS + API calls
           ↓
┌─────────────────────┐
│  Render Backend     │  https://reco-movies-backend.onrender.com
│  (Flask + Python)   │
└──────────┬──────────┘
           │ SQL queries
           ↓
┌──────────────────────┐
│ Render PostgreSQL    │  postgresql://...
│  (Database)          │
└──────────────────────┘
```

---

## 🔑 Secrets et Variables d'Environnement {#secrets}

### Backend (Render)
```
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/db
CORS_ORIGIN=https://[frontend-vercel].vercel.app
TMDB_API_KEY=ton_cle_api
```

### Frontend (Vercel)
```
VITE_API_URL=https://reco-movies-backend.onrender.com
VITE_APP_NAME=MyTflix
```

---

## 📝 Configuration fichiers (déjà ajoutés)

```
.github/
  workflows/
    backend-ci.yml          ✅ Tests Backend
    frontend-ci.yml         ✅ Tests Frontend

render.yaml                 ✅ Config Render
frontend/vercel.json        ✅ Config Vercel

requirements.txt            ✅ Python deps
requirements-dev.txt        ✅ Dev deps
```

---

## 🔄 Workflow de déploiement automatique

### Option 1: Automatique via GitHub (RECOMMANDÉ)

1. **Git push** → GitHub
2. **GitHub Actions** lance les tests
3. Si ✅ → Render/Vercel redéploient automatiquement

### Option 2: Manuel

```bash
# Render
git push origin main
# (Render redéploie auto si lié)

# Vercel
git push origin main
# (Vercel redéploie auto si lié)
```

---

## 🐛 Dépannage {#troubleshooting}

### ❌ Build fails sur Render

**Erreur típique:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Vérifie requirements.txt
cat requirements.txt

# Ajoute les dépendances manquantes
pip freeze > requirements.txt
git push origin main
```

### ❌ Frontend CORS error

**Erreur:**
```
Access to XMLHttpRequest blocked
```

**Solution:** Ajoute dans `.env` Vercel :
```
VITE_API_URL=https://reco-movies-backend.onrender.com
```

### ❌ Database connection failed

**Solution:**
```
1. Va sur Render → PostgreSQL
2. Copie la DATABASE_URL
3. Ajoute dans Backend Environment
4. Redémarre le service
```

### ❌ Port 0.0.0.0 error

**Solution:** Dans `app.py` :
```python
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

---

## 🧪 Test avant de déployer

```bash
# 1. Test local backend
FLASK_ENV=production python app.py

# 2. Test local frontend
cd frontend
npm run build
npm run preview

# 3. Vérifier health check
curl http://localhost:5000/health
```

---

## 📊 Monitoring et Logs

### Render
- Dashboard → Services → **Logs**
- Check l'onglet **Metrics**

### Vercel
- Dashboard → [Project] → **Deployments**
- Clique sur un deploy pour voir les logs
- **Analytics** pour voir les performances

---

## ✅ Checklist

- [ ] Créer compte Render
- [ ] Créer compte Vercel
- [ ] Lier repo GitHub
- [ ] Configurer Backend sur Render
- [ ] Créer PostgreSQL sur Render
- [ ] Ajouter DATABASE_URL au Backend
- [ ] Configurer Frontend sur Vercel
- [ ] Ajouter VITE_API_URL au Frontend
- [ ] Tester requêtes GET/POST
- [ ] Vérifier CORS
- [ ] Voir les logs de déploiement

---

## 🎉 Bravo !

Ton app est maintenant **live** et prête pour la prod ! 🚀

```
Frontend:  https://[ton-projet].vercel.app
Backend:   https://reco-movies-backend.onrender.com
```

---

## 📚 Ressources

- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [Flask + Gunicorn](https://gunicorn.org/)
- [Environment Variables](https://vercel.com/docs/projects/environment-variables)
