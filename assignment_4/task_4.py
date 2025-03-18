input_number = int(input("enter the number from 0 to 20: "))

result = 0
first_num = 0
second_num = 1

for i in range (1,input_number):
    result = first_num + second_num
    first_num = second_num
    second_num = result

print(f"მიმდევრობის n-ური წევრია: {result}")