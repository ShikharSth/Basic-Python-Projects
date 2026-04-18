## A simple calculator script that performs basic arithmetic operations.
# num1 = input("Enter the first number: ")
# try:
#     num1 = float(num1)
# except ValueError:
#     print("Invalid input, please enter valid numeric values!")
#     exit()

# num2 = input("Enter the second number: ")
# try:
#     num2 = float(num2)
# except ValueError:
#     print("Invalid input, please enter valid numeric values!")
#     exit()

# operation = input("Choose an operation (+, -, *, /, %): ")


# if operation == "+":
#     result = num1 + num2
# elif operation == "-":
#     result = num1 - num2
# elif operation == "*":
#     result = num1 * num2
# elif operation == "/":
#     try:
#         result = num1 / num2
#     except ZeroDivisionError:
#         result = "Error: Cannot devide by zero!"
# elif operation == "%":
#     result = num1 % num2
# else:
#     result = "Invalid operation"

# print(f"The result of {num1} {operation} {num2} is: {result}")


## A simple calculator app using tkinter GUI that performs basic arithmetic operations.
import tkinter as tk

def calculate(operator):
    num1 = entry1.get()
    num2 = entry2.get()

    try:
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        result_label.config(text="Invalid input, please enter valid numeric values!")
        return
    
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 == 0:
            result_label.config(text="Error: Cannot divide by zero!")
            return
        result = num1 / num2
    elif operator == "%":
        if num2 == 0:
            result_label.config(text="Error: Cannot modulo by zero!")
            return
        result = num1 % num2
    else:
        result_label.config(text="Unknown operation")
        return

    result_label.config(text=f"The result of {num1} {operator} {num2} is: {result}")
    
    
    

# main window
root = tk.Tk()
root.title("Simple Calculator 🧮")
root.geometry("600x250")

# make colums equal width
for i in range(5):
    root.grid_columnconfigure(i, weight=1)

# Input fields
label1 = tk.Label(root, text="First Number:")
label1.grid(row=0, column=0, padx=10, pady=10)
entry1 = tk.Entry(root, width=30)
entry1.grid(row=0, column=1, columnspan=4, padx=10, pady=10, sticky="ew")

label2 = tk.Label(root, text="Second Number:")
label2.grid(row=1, column=0, padx=10, pady=10)
entry2 = tk.Entry(root, width=30)
entry2.grid(row=1, column=1, columnspan=4, padx=10, pady=10, sticky="ew")

# buttons for operations
operators = ["+", "-", "x", "/", "%"]

for i, op in enumerate(operators):
    actual_op = "*" if op == "x" else op
    tk.Button(root, text=op, font=("Arial", 20),
              bg="gray", fg="black",
              command=lambda o=actual_op: calculate(o)
              ).grid(row=2, column=i, padx=5, pady=5, sticky="nsew")

# result label
result_label = tk.Label(root, text="Result:", font=("Arial", 14), bg="blue", width=50, fg="white")
result_label.grid(row=3, column=0, pady=10, padx=10, columnspan=5, sticky="ew")

# run app
root.mainloop()