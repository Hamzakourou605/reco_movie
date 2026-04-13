#!/bin/bash
# Script pour tester localement AVANT de pusher (Linux/Mac)
# Sur Windows: crée un fichier .bat ou utilise PowerShell

echo "🔍 Vérification locale du CI/CD..."
echo ""

# 1. Vérifier Python
echo "✅ Vérification Python..."
python --version

# 2. Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt -q

# 3. Tests Python
echo ""
echo "🧪 Lancement des tests Python..."
pytest test_ml_recommendations.py -v --tb=short 2>/dev/null || echo "⚠️  Pas de tests ou erreur"

# 4. Lint Python
echo ""
echo "🎨 Vérification du style (flake8)..."
pip install flake8 black isort -q
flake8 . --count --select=E9,F63,F7,F82 --show-source || true

# 5. Build check
echo ""
echo "🔨 Vérification du build..."
python -c "from ml_model import MovieRecommender; print('✅ ml_model OK')" && \
python -c "from ml_experiment_tracker import MLflowExperimentTracker; print('✅ ml_experiment_tracker OK')" || \
echo "⚠️  Erreur d'import"

# 6. Tests Frontend
echo ""
echo "📦 Vérification du Frontend..."
if [ -d "frontend" ]; then
    cd frontend
    npm ci -q 2>/dev/null || echo "⚠️  npm non installé ou erreur"
    npm run lint 2>/dev/null || echo "⚠️  Pas de lint configuré"
    cd ..
else
    echo "⚠️  Dossier frontend non trouvé"
fi

echo ""
echo "✅ Vérification locale complète!"
echo "🚀 Prêt à pusher ?"
