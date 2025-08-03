tasks = []

def show_menu():
    print("\n--- To-Do List Menu ---")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Done")
    print("4. Delete Task")
    print("5. Exit")

def add_task():
    task_input = input("Enter your task: ")
    tasks.append({"task": task_input, "done": False})
    print("Task added successfully")

def view_tasks():
    if not tasks:
        print("No task available")
    else:
        print("\n.....Task List.....")
        for i, t in enumerate(tasks):
            status = "Done" if t["done"] else "Not Done"
            print(f"{i+1}. {t['task']} - {status}")

def mark_done():
    view_tasks()
    if tasks:
        try:
            index = int(input("Enter task number: ")) - 1
            if 0 <= index < len(tasks):
                tasks[index]["done"] = True
                print("Task marked as done.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")

def delete_task():
    view_tasks()
    if tasks:
        try:
            index = int(input("Enter task number to delete: ")) - 1
            if 0 <= index < len(tasks):
                tasks.pop(index)
                print("Task deleted.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")

while True:
    show_menu()
    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        mark_done()
    elif choice == "4":
        delete_task()
    elif choice == "5":
        print("Exiting To-Do List App. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")