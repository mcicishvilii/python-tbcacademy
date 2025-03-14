import random

suits = ["hearts", "spades", "clubs", "diamonds"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

random_card = f"{random.choice(ranks)} of {random.choice(suits)}"

print(random_card)