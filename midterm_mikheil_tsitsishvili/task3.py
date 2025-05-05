import random

rps = ["R", "P", "S"]


def rand_RPS():
    return random.choice(rps)


def main():
    rand_rps = rand_RPS()
    user_input = input("rock, paper or scissors?: ").upper()

    print(f"useris sheyvanili: {user_input}")
    print(f"randomaizeris pasuxi: {rand_rps}")

    if user_input == "R" and rand_rps == "S":
        print("You won!")
    elif user_input == "R" and rand_rps == "P":
        print("You won!")
    elif user_input == "P" and rand_rps == "R":
        print("You won!")
    elif user_input == rand_rps:
        print("Draw!")
        main()


if __name__ == "__main__":
    main()
