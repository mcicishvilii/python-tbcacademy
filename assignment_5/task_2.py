for i in range(1, 10):
    line = ""
    j = 1
    while j <= i:
        line += f"{j} * {i} = {j * i}     "
        j += 1
    print(line)
