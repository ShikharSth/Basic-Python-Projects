inpt = input("Enter a string or number to check if it's a palindrome: ")

# remove spaces and conver to lowercase
new_inpt = inpt.replace(" ", "").lower()

reversed_inpt = new_inpt[::-1]

if new_inpt == reversed_inpt:
    print(f"{inpt} is a palindrome.")
else:
    print(f"{inpt} is not a palindrome.")
