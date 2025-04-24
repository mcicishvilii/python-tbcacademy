import random


def list_mult():
    original_list = [random.randint(1, 30) for _ in range(50)]

    expanded_list = []

    for number in original_list:
        expanded_list.extend([number] * number)

    print("ახალი სიის სიგრძე:", len(expanded_list))
    print("ახალი სია:", expanded_list)


def main():
    list_mult()


if __name__ == "__main__":
    main()
