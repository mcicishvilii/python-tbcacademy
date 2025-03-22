input_number = int(input("please enter the whole number from 1 to 50: "))
temp_number = 0
divisors = []

if input_number < 1 or input_number > 50:
    print("please enter number from 1 to 50")
else:
    while temp_number < input_number:
        temp_number += 1
        for i in range (1,temp_number + 1):
            if temp_number % i == 0:
                divisors.append(i)
            print(divisors)
                