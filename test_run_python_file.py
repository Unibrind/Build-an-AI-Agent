from functions.run_python_file import run_python_file

test_cases = [
    # (working_dir, file_path, args, description)
    ("calculator", "main.py", None, "Aide de l'application"),
    ("calculator", "main.py", ["3 + 5"], "Calcul simple"),
    ("calculator", "tests.py", None, "Exécution des tests internes"),
    ("calculator", "../main.py", None, "Tentative de sortie du dossier (Sécurité)"),
    ("calculator", "nonexistent.py", None, "Fichier qui n'existe pas"),
    ("calculator", "lorem.txt", None, "Fichier non-Python"),
]

for wd, path, args, desc in test_cases:
    print(f"--- TEST: {desc} ---".center(60, "-"))
    print(f"Appel: run_python_file('{wd}', '{path}', args={args})")
    
    resultat = run_python_file(wd, path, args)
    
    # Indentation pour la clarté
    print("  " + resultat.replace("\n", "\n  "))
    print("-" * 60 + "\n")