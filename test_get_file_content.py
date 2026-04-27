from functions.get_file_content import get_file_content

test_cases = [("calculator", "main.py"), ("calculator", "pkg/calculator.py"), ("calculator", "/bin/cat"), ("calculator", "pkg/does_not_exist.py"), ("calculator", "ggg")]

for i in test_cases:
    print(f"Result for {i[1]} directory:\n{get_file_content(i[0], i[1])}\n")