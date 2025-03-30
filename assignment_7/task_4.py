qwerty = "qwertyuiopasdfghjklzxcvbnm"

action = input("please enter 'e' to encrypt and 'd' to decrypt: ")
user_input = ""


def encrypt(user_input):
    counter = 0
    encrypted_text = ""
    while counter < len(user_input):
        if user_input[counter] in qwerty:
            index = qwerty.index(user_input[counter])
            new_index = (index + 1) % len(qwerty)
            encrypted_text += qwerty[new_index]
        else:
            encrypted_text += user_input[counter]
        counter += 1
    return encrypted_text


def decrypt(user_input):
    counter = 0
    decrypted_text = ""
    while counter < len(user_input):
        if user_input[counter] in qwerty:
            index = qwerty.index(user_input[counter])
            new_index = (index - 1) % len(qwerty)
            decrypted_text += qwerty[new_index]
        else:
            decrypted_text += user_input[counter]
        counter += 1
    return decrypted_text


if action == "e":
    user_input = input("please write a text to encrypt: ")
    print(encrypt(user_input))
elif action == "d":
    user_input = input("please enter the code to decrypt message: ")
    print(decrypt(user_input))
else:
    print("wrong action entered")
