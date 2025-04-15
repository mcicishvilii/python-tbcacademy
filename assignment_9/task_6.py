def car(manufacturer, year_of_make="2025", **kwargs):
    details = f"{manufacturer} - manufacturer\n{year_of_make} - yaer of make\n"
    for key, value in kwargs.items():
        details += f"{key} - {value}\n"
    return details


print(car("Honda", color="blue", type="roadster"))
print(car("Honda", "1997", color="blue", type="roadster", petrol="Diesel"))
