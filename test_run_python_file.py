from functions.run_python_file import run_python_file

test_cases = [
    ("calculator", "main.py"),
    ("calculator", "main.py", ["3 + 5"]),
    ("calculator", "tests.py"),
    ("calculator", "../main.py"),
    ("calculator", "nonexistent.py"),
    ("calculator", "lorem.txt")
]

for i in test_cases:
    print(f"Result for {i[1]} directory:\n{run_python_file(i[0], i[1], i[2] if len(i) > 2 else None)}\n")
