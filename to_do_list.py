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
    
    elif choice == '2':
        if to_do_list:
            print("\nYour To-Do List:")
            for idx, task in enumerate(to_do_list, start=1):
                print(f"{idx}. {task}")
        else:
            print("Your to-do list is empty.")
    
    elif choice == '3':
        if to_do_list:
            try:
                num = int(input("Enter the number of the task to remove: "))
                if 1 <= num <= len(to_do_list):
                    removed_task = to_do_list.pop(num - 1)
                    print(f"Task '{removed_task}' removed from the list.")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("Your to-do list might be empty.")
    
    

