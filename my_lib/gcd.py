def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def gcd_rec(a, b):
    if b == 0:
        return a
    else:
        return gcd_rec(b, a % b)

