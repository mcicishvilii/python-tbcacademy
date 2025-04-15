def is_prime(num):
    if num < 2:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True


print(is_prime(17)) # True
print(is_prime(78)) # False
print(is_prime(61)) # True
print(is_prime(95))  # False
