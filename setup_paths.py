# setup_paths.py
import os
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BANK_ACCOUNT_PATH = os.path.join(PROJECT_ROOT, "bank_account")

# --- Étape 1 : création des __init__.py manquants ---
def ensure_init_files():
    print("Vérification des __init__.py ...")
    for root, dirs, files in os.walk(BANK_ACCOUNT_PATH):
        if "__init__.py" not in files:
            init_path = os.path.join(root, "__init__.py")
            open(init_path, "a").close()
            print(f"Ajout de {init_path}")
    print("Tous les packages sont bien initialisés.\n")

# --- Étape 2 : ajout du PYTHONPATH ---
def ensure_pythonpath():
    current_path = os.environ.get("PYTHONPATH", "")
    if PROJECT_ROOT not in current_path.split(os.pathsep):
        os.environ["PYTHONPATH"] = PROJECT_ROOT + os.pathsep + current_path
        print(f"PYTHONPATH défini sur : {PROJECT_ROOT}")
    else:
        print("PYTHONPATH déjà correct.\n")

# --- Étape 3 : test d'import du module ---
def test_import():
    print("Test d'import du package 'bank_account' ...")
    try:
        import bank_account
        print("Import réussi du package bank_account 🎉\n")
    except Exception as e:
        print(f"Erreur d'import : {e}")
        sys.exit(1)

# --- Étape 4 : lancement optionnel du serveur FastAPI ---
def launch_fastapi():
    print("Lancement du serveur FastAPI ...\n")
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload"])


# --- Exécution séquentielle ---
if __name__ == "__main__":
    ensure_init_files()
    ensure_pythonpath()
    test_import()

    choice = input("Souhaitez-vous lancer le serveur FastAPI maintenant ? (o/n) : ").strip().lower()
    if choice == "o":
        launch_fastapi()
    else:
        print("Configuration terminée. Vous pouvez lancer manuellement avec :")
        print("   uvicorn bank_account.main:app --reload")
