number = int(input("gtxovt sheiyvanot ricxvi 1-9 chatvlit: "))
divisors = ""
if number > 10:
    print("gtxovt sheiyvanot ricxvi 1 dan 9is chatvlit!!!")
elif number == 0:
    print("gtxovt sheiyvanot ricxvi 1 dan 9is chatvlit!!! nuls araqvs gamyopi")
else:
    if number % 2 == 0:
        divisors = divisors + " 2"
    if number % 3 == 0:
        divisors = divisors + " 3"    
    if number % 4 == 0:
        divisors = divisors + " 4"
    if number % 5 == 0:
        divisors = divisors + " 5"
    if number % 6 == 0:
        divisors = divisors + " 6"
    if number % 7 == 0:
        divisors = divisors + " 7"
    if number % 8 == 0:
        divisors = divisors + " 8"
    if number % 9 == 0:
        divisors = divisors + " 9"
print(divisors)