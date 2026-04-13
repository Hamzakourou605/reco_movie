# ⚡ Déployer sur Render - Quick & Simple

## 🚀 5 étapes en 15 minutes

### 1️⃣ Compte Render (2 min)

```
https://render.com
↓
Sign up with GitHub
↓
Authorize GitHub
✅
```

---

### 2️⃣ Web Service (5 min)

**Dashboard** → **New +** → **Web Service**

```
┌──────────────────────────────┐
│ Import from GitHub           │
│ Cherches: reco_movie         │
│ Clique: SELECT               │
└──────────────────────────────┘
```

**Configure:**

| Champ | Valeur |
|-------|--------|
| Name | `reco-movies-backend` |
| Branch | `main` |
| Runtime | `Python 3.11` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT` |
| Plan | `Free` |

```
Advanced Settings
↓
Add Environment Variable:
FLASK_ENV = production
↓
Create Web Service
```

**Attends: ~5-10 min** ⏱️

---

### 3️⃣ PostgreSQL Database (3 min)

**Dashboard** → **New +** → **PostgreSQL**

```
Database Name: reco_movies
User: postgres
Region: Singapore
Plan: Free
↓
Create Database
```

**Copie l'External URL:**
```
postgresql://user:xxx@dpg-xxxxx.onrender.com/reco_movies
```

---

### 4️⃣ Ajouter DATABASE_URL (2 min)

**Web Service** → **Environment**

```
Add New:
DATABASE_URL = [Copie External URL]
↓
Save
↓
Manual Deploy → Deploy latest commit
```

**Attends: ~3-5 min** ⏱️

---

### 5️⃣ Tester (3 min)

**Web Service → Logs**

```
Attends "Server running" ✅
```

**Tester l'API:**

```bash
curl https://reco-movies-backend-xxxxx.onrender.com/health

# Réponse: {"status":"healthy"}
```

---

## 🎉 C'est fait!

```
URL Backend: https://reco-movies-backend-xxxxx.onrender.com
URL Database: postgresql://...
```

---

## 🔗 Prochaines étapes

1. Copie l'URL backend
2. Va déployer le frontend sur Vercel (guide séparé)
3. Configure CORS dans le frontend

---

## 🐛 Si ça ne marche pas

| Problème | Solution |
|----------|----------|
| Build fails | Vérifier `requirements.txt` |
| App crashes | Voir les Logs |
| DB connection error | Vérifier `DATABASE_URL` |
| 503 Service | Attendre 1-2 min |

---

## 📚 Plus de détails?

Voir: [DEPLOY_RENDER_STEP_BY_STEP.md](DEPLOY_RENDER_STEP_BY_STEP.md) (guide complet)

---

**✅ À toi de jouer ! 🚀**
