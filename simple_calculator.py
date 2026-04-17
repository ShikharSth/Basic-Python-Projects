num1 = input("Enter the first number: ")
try:
    num1 = float(num1)
except ValueError:
    print("Invalid input, please enter valid numeric values!")
    exit()

num2 = input("Enter the second number: ")
try:
    num2 = float(num2)
except ValueError:
    print("Invalid input, please enter valid numeric values!")
    exit()

operation = input("Choose an operation (+, -, *, /, %): ")


if operation == "+":
    result = num1 + num2
elif operation == "-":
    result = num1 - num2
elif operation == "*":
    result = num1 * num2
elif operation == "/":
    try:
        result = num1 / num2
    except ZeroDivisionError:
        result = "Error: Cannot devide by zero!"
elif operation == "%":
    result = num1 % num2
else:
    result = "Invalid operation"

print(f"The result of {num1} {operation} {num2} is: {result}")
