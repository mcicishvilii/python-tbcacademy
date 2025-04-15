def factorial_calculator(num):
    mult = 1
    for i in range(1, num + 1):
        mult = mult * i
    return mult


print(factorial_calculator(6))  # 720
print(factorial_calculator(7))  # 5040
print(factorial_calculator(8))  # 40320
