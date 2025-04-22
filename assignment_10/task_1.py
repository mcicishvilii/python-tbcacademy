def temp_conversion(unit_from, number):
    answer = 0
    if unit_from.lower() == "c":
        answer = number * 9 / 5 + 32
        return f"{int(answer)} F"
    elif unit_from.lower() == "f":
        answer = (number - 32) * 5 / 9
        return f"{int(answer)} C"
    else:
        return "please enter either C or F"


unit_from = input("please enter the unit to convert from: ")
number = int(input("please input temperature: "))

print(temp_conversion(unit_from, number))
