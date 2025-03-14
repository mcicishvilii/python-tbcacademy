car_speed = int(input("manqanis sichqarea: "))

if car_speed < 30 and car_speed > 0:
    print("SLOW")
elif car_speed >= 30 and car_speed < 60:
    print("MODERATE")
elif car_speed >= 60 and car_speed < 120:
    print("FAST")
elif car_speed >= 120:
    print("VERY FAST!!!")