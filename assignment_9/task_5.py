def reverse_text(text):
    test_word = ""
    for char in text[::-1]:
        test_word += char
    return test_word


print(reverse_text("hello world!"))  # !dlrow olleh
print(reverse_text("Bob Dylan"))  # nalyD boB
print(reverse_text("I love Python so much!"))  # !hcum os nohtyP evol I
print(reverse_text("radar"))  # radar
