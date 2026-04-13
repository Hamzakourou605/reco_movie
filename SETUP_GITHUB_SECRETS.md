# 🔑 Setup des Secrets GitHub

Pour activer le déploiement automatique, tu dois ajouter des secrets dans GitHub.

## 📝 Secrets à ajouter

Va sur : **GitHub Repo** → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

---

## 🎯 Pour Render (Backend)

### 1. `RENDER_SERVICE_ID`
- Va sur Render Dashboard
- Sélectionne ton service Backend
- Copie l'ID de la barre d'URL : `srv-xxxxx`
- Ajoute dans GitHub Secrets

### 2. `RENDER_DEPLOY_KEY`
- Render Dashboard → **Account Settings** → **API Keys**
- Clique **"Create API Key"**
- Copie la clé → GitHub Secrets

---

## 🎨 Pour Vercel (Frontend)

### 1. `VERCEL_TOKEN`
```bash
# Option 1: Via CLI
vercel login
vercel link
vercel env pull

# Option 2: Manuellement
# Va sur: https://vercel.com/account/tokens
# Create Token → Copy → GitHub Secrets
```

### 2. `VERCEL_ORG_ID`
```bash
vercel env pull
# Regarde le fichier .vercel/project.json
# Copie: "orgId": "xxxxx"
```

### 3. `VERCEL_PROJECT_ID`
```bash
# Dans .vercel/project.json
# Copie: "projectId": "xxxxx"
```

---

## ✅ Checklist

- [ ] Créer RENDER_SERVICE_ID
- [ ] Créer RENDER_DEPLOY_KEY
- [ ] Créer VERCEL_TOKEN
- [ ] Créer VERCEL_ORG_ID
- [ ] Créer VERCEL_PROJECT_ID
- [ ] Tester un `git push` vers main

---

## 🧪 Test du déploiement

```bash
# 1. Ajouter les secrets
# (fait via GitHub UI)

# 2. Pusher une modification
git add .
git commit -m "Test: CI/CD deployment"
git push origin main

# 3. Vérifier
# GitHub → Actions → Voir le workflow
# Si ✅, tes services seront déployés auto
```

---

## 🐛 Dépannage

### ❌ Deploy fails: "Invalid API key"
- Vérifie que RENDER_DEPLOY_KEY est correct
- Régénère la clé sur Render si nécessaire

### ❌ Deploy fails: "Service not found"
- Vérifie RENDER_SERVICE_ID
- Format: `srv-xxxxxxxxxxxxx`

### ❌ Vercel deploy fails: "Unauthorized"
- Régénère VERCEL_TOKEN sur Vercel Dashboard
- Assure-toi que tu as les permissions

---

## 📚 Ressources

- [Render API Keys](https://render.com/docs/api-reference#authentication)
- [Vercel Tokens](https://vercel.com/docs/rest-api#authentication/project-endpoints)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

---

Une fois configuré, ton pipeline est complètement automatisé ! 🚀
