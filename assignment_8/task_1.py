input_word = input("please enter the string: ")

test_word = ""
input_word_new = ""

for char in input_word[::-1]:
    if char.isalpha():
        test_word += char

for char in input_word:
    if char.isalpha():
        input_word_new += char

if test_word.lower() == input_word_new.lower():
    print("Is palindrome")
else:
    print("Is Not a palindrome")