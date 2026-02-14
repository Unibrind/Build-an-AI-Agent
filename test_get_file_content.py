from functions.get_file_content import get_file_content

test_cases = [
    ("calculator", "main.py", "main.py file"),
    ("calculator", "pkg/calculator.py", "'pkg/calculator.py' file"),
    ("calculator", "/bin/cat", "'/bin/cat' file"),
    ("calculator", "pkg/does_not_exist.py", "'pkg/does_not_exist.py' file"),
]

for worworking_directory, directory, description in test_cases:
    print()
    print(f"Result for {description}:")
    resultat = get_file_content(worworking_directory, directory)
    print("  " + resultat.replace("\n", "\n  "))
    print("\n"+"------" * 10)