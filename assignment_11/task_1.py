def avg_temp():
    temperatures = [22, 25, 19, 23, 25, 26, 23]

    total = 0

    for temp in temperatures:
        total += temp

    average = total / len(temperatures)

    print("საშუალო ტემპერატურაა:", round(average, 1))


def main():
    avg_temp()
    return


if __name__ == "__main__":
    main()
