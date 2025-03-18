import random

input_number = int(input("please enter the whole number: "))
random_num = random.randint(0,1000)
higher_or_lower = ""

if (0 < input_number < 30):
    if(input_number > random_num):
        higher_or_lower = "is higher than "
    elif (input_number < random_num):
        higher_or_lower = "is lower than "
    else:
        higher_or_lower = "is equal to "
    print(f"random number generated was: {random_num} and the number you entered {higher_or_lower} {random_num}")
else:
    print("please enter number from 1 to 30")