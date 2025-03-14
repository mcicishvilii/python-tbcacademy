from datetime import datetime 

year_of_birth = input("please enter the year of your birth: ")
month_of_birth = input("please enter the month of your birth: ")
day_of_birth = input("please enter the day of your birth: ")

# მომხმარებელი თუ შეიყვანს 02 ან 2 ორივე შემთხვევაში იმუშავებს
if len(month_of_birth) == 1:
    month_of_birth = f"0{month_of_birth}"

# აქაც იგივე
if len(day_of_birth) == 1:
    day_of_birth = f"0{day_of_birth}"


date_string = f"{year_of_birth}-{month_of_birth}-{day_of_birth}"
date_object = datetime.strptime(date_string, "%Y-%d-%m")

print(date_object.strftime("%A"))