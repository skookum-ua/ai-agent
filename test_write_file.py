from functions.write_file import write_file

test_cases = [("calculator", "lorem.txt", "wait, this isn't lorem ipsum"), ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"), ("calculator", "/tmp/temp.txt", "this should not be allowed")]

for i in test_cases:
    print(f"Result for {i[1]} directory:\n{write_file(i[0], i[1], i[2])}\n")