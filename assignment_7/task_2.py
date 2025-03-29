input_word = input("Please enter the word: ")

for i in input_word:
    if i in ("a", "e", "i", "o", "u"):
        print(end="")
    else:
        print(i, end="")
