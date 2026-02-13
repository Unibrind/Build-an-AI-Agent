from functions.get_files_info import get_files_info

test_cases = [
    ("calculator", ".", "current directory"),
    ("calculator", "pkg", "'pkg' directory"),
    ("calculator", "/bin", "'/bin' directory"),
    ("calculator", "../", "'../' directory"),
]

for worworking_directory, directory, description in test_cases:
    print()
    print(f"Result for {description}:")
    resultat = get_files_info(worworking_directory, directory)
    print("  " + resultat.replace("\n", "\n  "))
    print("\n"+"------" * 10)