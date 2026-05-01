to_do_list = []

while True:
    print("\n--- To-Do List ---")
    print("1. Add a Task")
    print("2. View Tasks")
    print("3. Remove a Task")
    print("4. Exit")

    choice = input("Choose an option (1-4): ")

    if choice == '1':
        task = input("Enter a task to add: ")
        to_do_list.append(task)
        print(f"Task '{task}' added to the list.")
    
    
