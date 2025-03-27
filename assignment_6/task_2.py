input_number = int(input("please enter number from 1 to 1000: "))
answer = 1
list = [f"{input_number} -> "]

if 1 < input_number > 1000:
    print("dzginkiani xar")
else:
    while input_number != answer:
        if input_number % 2 == 0:
            input_number /= 2
        else:
            input_number = input_number * 3 + 1
        list.append(f"{int(input_number)} -> ")

if len(list) == 1:
    print()
else:
    print("".join(list).rstrip(" -> "))
