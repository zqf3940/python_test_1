def reverse(text):
    return text[::-1]

def is_palinrome(text):
    return text == reverse(text)

something = input("Enter text: ")
if is_palinrome(something):
    print("yes, is is a palindrome")
else:
    print("no, is is not a palindrome")