import random

attempts = 0
random_number = random.randint(0, 100)

while attempts < 10:
    input_number = int(input("enter number: "))
    if input_number > random_number:
        print("high")
    elif input_number < random_number:
        print("low")
    else:
        print("you are winner!")
        break
    attempts += 1
    if attempts == 10:
        print("computer is winner")
        break
