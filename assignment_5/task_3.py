input_number = int(input("enter the number from 0 to 20: "))

result = 0
first_num = 0
second_num = 1
counter = 0

if input_number < 0 or input_number > 20:
    print("please enter number from 0 to 20")
else:
    if input_number == 0:
        print("მიმდევრობის n-ური წევრია: 0")
    else:
        print("", end=" ")
        while counter < input_number:
            print(result, end=" ")
            result = first_num + second_num
            first_num = second_num
            second_num = result
            counter += 1
