input = int(input("enter number from 1 to 10: "))
counter = input

if 1 < input < 10:
    while counter != 0:
        counter -= 1
        print("")
        for i in range(1, (input + 1) - counter):
            print(i, end=" ")
    print("", end="")
    while counter != input:
        counter += 1
        print("")
        for i in range(1, (input + 1) - counter):
            print(i, end=" ")
else:
    print("please enter 1 to 10")
