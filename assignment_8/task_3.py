date = "2024-03-22T03:17:42.966376-03:00"

year = date[0:4]
month = date[5:7]
day = date[8:10]
hr = date[11:13]
if int(hr) > 12:
    hr = int(hr) - 12
min = date[14:16]
sec = date[17:19]
ms = date[20:26]
timezone = date[26:29].replace("0", "")

example = f"{day}-{month}-{year} {hr}:{min}:{sec} {timezone}"

print(example)
