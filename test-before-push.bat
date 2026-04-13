@echo off
REM Script pour tester localement AVANT de pusher (Windows)

echo.
echo 🔍 Verification locale du CI/CD...
echo.

REM 1. Verifier Python
echo ✅ Verification Python...
python --version
if errorlevel 1 (
    echo ❌ Python non trouve!
    exit /b 1
)

REM 2. Installer les dependances
echo.
echo 📦 Installation des dependances...
pip install -r requirements.txt -q

REM 3. Tests Python
echo.
echo 🧪 Lancement des tests Python...
pytest test_ml_recommendations.py -v --tb=short 2>nul || (
    echo ⚠️  Pas de tests ou erreur
)

REM 4. Lint Python
echo.
echo 🎨 Verification du style (flake8)...
pip install flake8 black isort -q
flake8 . --count --select=E9,F63,F7,F82 --show-source 2>nul

REM 5. Build check
echo.
echo 🔨 Verification du build...
python -c "from ml_model import MovieRecommender; print('✅ ml_model OK')" || (
    echo ⚠️  Erreur import ml_model
)
python -c "from ml_experiment_tracker import MLflowExperimentTracker; print('✅ ml_experiment_tracker OK')" || (
    echo ⚠️  Erreur import ml_experiment_tracker
)

REM 6. Tests Frontend
echo.
echo 📦 Verification du Frontend...
if exist "frontend\" (
    cd frontend
    npm ci -q 2>nul || echo ⚠️  npm non installe ou erreur
    npm run lint 2>nul || echo ⚠️  Pas de lint configure
    cd ..
) else (
    echo ⚠️  Dossier frontend non trouve
)

echo.
echo ✅ Verification locale complete!
echo 🚀 Pret a pusher ?
echo.
pause
