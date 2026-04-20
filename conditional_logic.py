# genrate randim number adn let the user guess it with limited attempts
import random
random_number = random.randint(1, 100)
attempts = 5

print("Welcome to the Number Guessing Game!")
print(f"I'm thinking of a number between 1 and 100. You have {attempts} attempts...")

while attempts > 0:
    guess = input("Entet your number: ")

    try:
        guess = int(guess)
    except ValueError:
        print("Invalid input, please enter a valid number!")
        continue

    if guess < random_number:
        print("Too low! Try again with higher number.")
    elif guess > random_number:
        print("Too high! Try again with lowwer number.")
    else:
        print(f"Congratulations! You've guessed the number {random_number} correctly!")
        break

    attempts -= 1
    print(f"You have {attempts} attempts left.")

if attempts == 0:
    print(f"Game Over! The number I was thinking of was: {random_number}.")




# import tkinter as tk
# import random

# random_number = random.randint(1, 100)
# attempts = 5

# def check_guess():
#     global attempts

#     try:
#         guess = int(entry.get())
#     except ValueError:
#         result_label.config(text="Invalid input! Enter a number.")
#         return

#     attempts -= 1

#     if guess < random_number:
#         result_label.config(text=f"Too low! Attempts left: {attempts}")
#     elif guess > random_number:
#         result_label.config(text=f"Too high! Attempts left: {attempts}")
#     else:
#         result_label.config(text=f"🎉 Correct! Number was {random_number}")
#         return

#     if attempts == 0:
#         result_label.config(text=f"Game Over! Number was {random_number}")


# # UI
# root = tk.Tk()
# root.title("Random Number Guessing Game")
# root.geometry("500x300")

# for i in range(2):
#     root.grid_columnconfigure(i, weight=1)

# label1 = tk.Label(root, text="Welcome to the Number Guessing Game")
# label1.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

# label2 = tk.Label(root, text=f"I'm thinking of a number between 1 to 100. You have {attempts} attempts.")
# label2.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

# entry = tk.Entry(root)
# entry.grid(row=2, column=0, padx=10, pady=10)

# button = tk.Button(root, text="Guess", command=check_guess)
# button.grid(row=2, column=1, padx=10, pady=10)

# result_label = tk.Label(root, text="")
# result_label.grid(row=3, column=0, columnspan=2, pady=10)

# root.mainloop()