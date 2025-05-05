def main():
    input_number = int(input("please input the number from 10 to 5432: "))

    if 10 <= input_number <= 5432:
        all_correct_numbers = []
        for i in range(0, input_number):
            if i % 13 == 0:
                all_correct_numbers.append(i)
        print(f"ყველა 13-ის ჯერადი რიცხვი: {all_correct_numbers[1:]}")
        print(f"13-ის ჯერადი რიცხვების ჯამი: {len(all_correct_numbers) - 1}")

    else:
        print("entered incorrect number...")
        main()


if __name__ == "__main__":
    main()
