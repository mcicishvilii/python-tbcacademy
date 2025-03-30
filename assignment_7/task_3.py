import time

input_word = input("please enter the word: ")
count = 0
first_letter = ""
middle_letter = ""
mid_letter_if_even = ""
last_letter = ""
print_amount = 5


while count < len(input_word):
    first_letter = input_word[0]
    if len(input_word) % 2 != 0:
        middle_letter = input_word[int(len(input_word) / 2)]
    else:
        middle_letter = (
            input_word[int(len(input_word) / 2) - 1]
            + input_word[int(len(input_word) / 2)]
        )
    last_letter = input_word[-1]
    count += 1

for i in range(1, print_amount + 1):
    print(i, "...")
    time.sleep(1)
    print("first letter is: ", first_letter)
    print("middle letter is: ", middle_letter)
    print("last letter is: ", last_letter)
