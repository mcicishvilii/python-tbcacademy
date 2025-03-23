height = int(input("please enter the height from 1 to 50: "))
asterisks_count = 0
if height < 1 or height > 50:
    print("please enter the height from 1 to 50")
else:
    for i in range(1, height + 1):
        spaces = " " * (height - i)
        asterisks_count += 1
        asterisks = "*" * (asterisks_count)
        slashes = "/" * i
        backslashes = "\\" * i
        print(spaces + slashes  + asterisks + backslashes)
