from functions.write_file import write_file

test_cases = [
    ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("calculator", "/tmp/temp.txt", "this should not be allowed"),
]

for working_directory, file_path, content in test_cases:
    print()
    print(f"Result for {file_path}:")
    resultat = write_file(working_directory, file_path, content)
    print("  " + resultat.replace("\n", "\n  "))
    print("\n"+"------" * 10)