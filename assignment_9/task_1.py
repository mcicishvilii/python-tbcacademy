def vowel_count(user_input):
    counter = 0
    for i in user_input:
        if i in "aeiouAEIOU":
            counter += 1
    return counter


user_input = input("please enter a sentence: ")
print(vowel_count(user_input))