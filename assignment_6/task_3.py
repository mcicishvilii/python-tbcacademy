n = int(input("Enter a number (0 <= n < 10000): "))

reversed_num = 0
sum_digits = 0
original_n = n

while n > 0:
    last_digit = n % 10
    sum_digits += last_digit
    reversed_num = reversed_num * 10 + last_digit
    n //= 10

print(f"reversed number is {reversed_num}")
print(f"sum of digits: {sum_digits}")
