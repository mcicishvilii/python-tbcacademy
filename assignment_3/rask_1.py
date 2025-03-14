import math

number_to_power = int(input("please enter the number: "))
power = int(input("please enter the power: "))

powered_number = math.pow(number_to_power,power)

print(f"the the value of {number_to_power} raised to the power of {power} is: {int(powered_number)}")