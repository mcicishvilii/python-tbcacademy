input_word = input("please enter the string: ")

test_word = ""
input_word_new = ""

for i in input_word[::-1]:
    if i.isalpha():
        test_word = test_word + i

for i in input_word:
    if i.isalpha():
        input_word_new = input_word_new + i

if test_word.lower() == input_word_new.lower():
    print("Is palindrome")
else:
    print("Is Not a palindrome")
