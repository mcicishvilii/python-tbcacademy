
def remove_duplicates_from_list(list):
    new_list = []
    for i in list:
        if i not in new_list:
            new_list.append(i)
    return new_list

def main():
    list = [2, 1, 4, 2, 1]
    print(remove_duplicates_from_list(list))


if __name__ == "__main__":
    main()
