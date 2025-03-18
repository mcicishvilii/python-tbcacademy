import random

number_of_players = int(input("please enter the number of players: "))

for i in range(0,number_of_players):
    first_dice = random.randint(1, 6)
    second_dice =  random.randint(1, 6)
    print(f"{first_dice}:{second_dice}")