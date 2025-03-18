input_number = int(input("please enter the whole number from 1 to 1000: "))

if (0 < input_number < 1000):
    for i in range(1,input_number + 1):
        if (input_number % i == 0):
            print(i, end=" ")
else:
    print("please enter number from 1 to 1000")