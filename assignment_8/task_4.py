word = input("please enter the first word: ")
second_word = input("please enter the second word: ")

if sorted(word) == sorted(second_word):
    print("YES")
else:
    print("NO")