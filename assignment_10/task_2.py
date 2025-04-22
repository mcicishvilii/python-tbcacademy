import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from my_lib import gcd, gcd_rec


def calculate_lcm(a, b):
    return f" LCM of {a} and {b} is {int((a*b)/gcd_rec(a,b))}"


start_time = time.time()
print(calculate_lcm(1000, 400))
print(calculate_lcm(500, 50))
end_time = time.time()
execution_time = end_time - start_time

print(f"Program execution time: {execution_time} seconds")

# rekursiuli = 0.0016-21
# ararekursi = 0.0007-14
