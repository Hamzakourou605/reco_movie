"""
Script de test et vérification de l'intégration MLflow
Vérifie que MLflow est correctement configuré et fonctionnel
"""

import os
import sys
import json
from pathlib import Path

def test_mlflow_installation():
    """Test 1: Vérifier que mlflow est installé"""
    print("📦 Test 1: Installation MLflow...")
    try:
        import mlflow
        print(f"  ✅ MLflow {mlflow.__version__} installé")
        return True
    except ImportError:
        print("  ❌ MLflow non installé. Exécute: pip install mlflow")
        return False


def test_tracker_import():
    """Test 2: Importer la classe tracker"""
    print("\n📚 Test 2: Import du tracker...")
    try:
        from ml_experiment_tracker import MLflowExperimentTracker
        print("  ✅ MLflowExperimentTracker importé")
        return True
    except Exception as e:
        print(f"  ❌ Erreur import: {e}")
        return False


def test_tracker_initialization():
    """Test 3: Initialiser le tracker"""
    print("\n🎯 Test 3: Initialisation du tracker...")
    try:
        from ml_experiment_tracker import MLflowExperimentTracker
        tracker = MLflowExperimentTracker(
            experiment_name="Test Experiment",
            tracking_uri="./mlruns_test"
        )
        print("  ✅ Tracker initialisé")
        return True, tracker
    except Exception as e:
        print(f"  ❌ Erreur initialisation: {e}")
        return False, None


def test_mlruns_created():
    """Test 4: Vérifier que mlruns/ existe"""
    print("\n📁 Test 4: Répertoire mlruns...")
    mlruns_path = Path("./mlruns")
    if mlruns_path.exists():
        print(f"  ✅ Répertoire {mlruns_path} créé")
        # Lister les expériences
        experiments = list(mlruns_path.glob("*"))
        print(f"     ({len(experiments)} expériences trouvées)")
        return True
    else:
        print(f"  ⚠️  {mlruns_path} n'existe pas encore (créé après premier run)")
        return True  # Ce n'est pas un erreur


def test_train_script_exists():
    """Test 5: Vérifier que train_and_track.py existe"""
    print("\n🚀 Test 5: Script de training...")
    train_script = Path("train_and_track.py")
    if train_script.exists():
        print("  ✅ train_and_track.py existe")
        return True
    else:
        print("  ❌ train_and_track.py non trouvé")
        return False


def test_requirements():
    """Test 6: Vérifier les dépendances dans requirements.txt"""
    print("\n📋 Test 6: Dépendances...")
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
        
        required = ["mlflow", "pandas", "numpy", "scikit-learn", "Flask"]
        found = {pkg: pkg in content for pkg in required}
        
        all_found = all(found.values())
        
        for pkg, status in found.items():
            status_symbol = "✅" if status else "❌"
            print(f"  {status_symbol} {pkg}")
        
        return all_found
    except Exception as e:
        print(f"  ❌ Erreur lecture requirements.txt: {e}")
        return False


def test_dev_requirements():
    """Test 7: Vérifier requirements-dev.txt"""
    print("\n📋 Test 7: Dépendances dev...")
    dev_req = Path("requirements-dev.txt")
    if dev_req.exists():
        print("  ✅ requirements-dev.txt existe")
        return True
    else:
        print("  ⚠️  requirements-dev.txt n'existe pas ")
        return True


def test_basic_run():
    """Test 8: Lancer un run MLflow basique"""
    print("\n🧪 Test 8: Run MLflow basique...")
    try:
        import mlflow
        
        with mlflow.start_run(run_name="test_run"):
            mlflow.log_param("test_param", "test_value")
            mlflow.log_metric("test_metric", 0.95)
            mlflow.set_tag("test_tag", "verification")
        
        print("  ✅ Run MLflow complété")
        return True
    except Exception as e:
        print(f"  ❌ Erreur run: {e}")
        return False


def test_config_files():
    """Test 9: Vérifier fichiers de config"""
    print("\n⚙️  Test 9: Fichiers de configuration...")
    files_to_check = {
        "render.yaml": "Config Render",
        "frontend/vercel.json": "Config Vercel",
        ".github/workflows/backend-ci.yml": "Backend CI/CD",
        ".github/workflows/frontend-ci.yml": "Frontend CI/CD",
    }
    
    all_found = True
    for file_path, description in files_to_check.items():
        if Path(file_path).exists():
            print(f"  ✅ {description} ({file_path})")
        else:
            print(f"  ⚠️  {description} non trouvé")
    
    return all_found


def test_documentation():
    """Test 10: Vérifier documentation"""
    print("\n📖 Test 10: Documentation...")
    docs = {
        "CI_CD_GUIDE.md": "Guide CI/CD",
        "DEPLOY_RENDER_VERCEL.md": "Guide déploiement",
        "SETUP_GITHUB_SECRETS.md": "Setup secrets",
    }
    
    for doc_file, description in docs.items():
        if Path(doc_file).exists():
            print(f"  ✅ {description}")
        else:
            print(f"  ⚠️  {description} non trouvé")


def generate_report(results):
    """Générer un rapport de test"""
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    passed = sum(1 for r in results if r)
    total = len(results)
    percentage = (passed / total) * 100
    
    print(f"\n✅ Réussis: {passed}/{total} ({percentage:.0f}%)")
    
    if percentage == 100:
        print("\n🎉 Tous les tests passés! MLflow est prêt!")
        print("\n🚀 Prochaines étapes:")
        print("   1. Exécuter: python train_and_track.py")
        print("   2. Visualiser: mlflow ui")
        print("   3. Ouvrir: http://localhost:5000")
    elif percentage >= 80:
        print("\n⚠️  Quelques tests manquants. Vérifiez les détails.")
    else:
        print("\n❌ Plusieurs tests ont échoué. Vérifiez la configuration.")
    
    return percentage


def main():
    """Exécuter tous les tests"""
    print("\n" + "="*60)
    print("🧪 VÉRIFICATION DE L'INTÉGRATION MLFLOW")
    print("="*60 + "\n")
    
    results = []
    
    # Exécuter les tests
    results.append(test_mlflow_installation())
    results.append(test_tracker_import())
    test3_result, tracker = test_tracker_initialization()
    results.append(test3_result)
    results.append(test_mlruns_created())
    results.append(test_train_script_exists())
    results.append(test_requirements())
    results.append(test_dev_requirements())
    results.append(test_basic_run())
    test_config_files()
    test_documentation()
    
    # Générer rapport
    percentage = generate_report(results)
    
    print("\n" + "="*60)
    
    return 0 if percentage >= 80 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
