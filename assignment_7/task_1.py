input_string = input("Please enter a sentence: ")

for i in range(len(input_string)):
    if i % 2 == 0 and input_string[i] != "e":
        print(input_string[i], end="")
else:
    print()
