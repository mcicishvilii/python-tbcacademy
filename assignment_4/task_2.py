import random

input_number = int(input("please enter the whole number: "))
list_of_numbers = []

for i in range (0, input_number):
    list_of_numbers.append(random.randint(0, 100)) 

print(f"the maximum number from the {input_number} randomly generated numbers is {max(list_of_numbers)}")