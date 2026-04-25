# take list input from user and print all even numbers

lst = input("Enter a list of numbers separated by spaces: ").split()

# print(lst)

even_numbers = [num for num in lst if num.isdigit() and int(num) % 2 == 0]

print("Even numbers in the List:", even_numbers)
