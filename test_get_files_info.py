from functions.get_files_info import get_files_info

test_cases = [("calculator", "."), ("calculator", "pkg"), ("calculator", "/bin"), ("calculator", "../"), ("calculator", "ggg")]

for i in test_cases:
    print(f"Result for {i[1]} directory:\n{get_files_info(i[0], i[1])}\n")