### A program to count the number of vowels in a user-provided sentence.

#--- Basic vowel counting program ---#
# sentence = input("Enter a sentence: ")
# vowels = "aeiouAEIOU"

# vowel_count = 0

# for char in sentence:
#     if char in vowels:
#         vowel_count += 1

# print(f"The number of vowels in the sentence is: {vowel_count}")

#--- basic tkinter app ---#
# import tkinter as tk

# root = tk.Tk()
# root.title("My First App")
# root.geometry("300x200")

# root.mainloop()


#--- Vowel counting app with tkinter ---#
import tkinter as tk

def count_vowels():
    sentence = entry.get()
    vowels = "aeiouAEIOU"

    vowel_count = sum(1 for char in sentence if char in vowels)

    # vowel_count = 0
    # for char in sentence:
    #     if char in vowels:
    #         vowel_count += 1

    result_label.config(text="Vowels: " + str(vowel_count))

root = tk.Tk()
root.title("Vowel Counter App")
root.geometry("400x200")

# make colums equal width
for i in range(2):
    root.grid_columnconfigure(i, weight=1)


label = tk.Label(root, text="Enter a sentence:")
label.grid(row=0, column=0, padx=5, pady=5)

entry = tk.Entry(root, width=30)
entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

button = tk.Button(root, text="Count Vowels", font=("Arial", 14), bg="green", fg="blue", height=1, command=count_vowels)
button.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

result_label = tk.Label(root, text="Vowels: 0", font=("Arial", 12), bg="blue", fg="white")
result_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

root.mainloop()
