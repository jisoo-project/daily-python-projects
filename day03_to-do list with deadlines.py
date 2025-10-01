tasks = []

def add_task():
    task = input("Enter the task: ")
    deadline = input("Is there any deadline?(yes/no): ")
    date = "No deadline"
    if deadline.lower() == "yes":
        date = input("When is the deadline?(year-month-day): ")
    tasks.append({"task":task, "deadline":date, "done":False})

def view_task():
    if not tasks:
        print("No tasks yet.")
    else:
        for i, task in enumerate(tasks, start=1):
            if task["done"]:
                status = "✅"
            else:
                status = " "
            print(f"{i}. [{status}] {task['task']} (deadline: {task['deadline']})")

def complete_task():
    if not tasks:
        print("There are no tasks yet.")
    else:
        try:
            done = int(input("Enter the number of the task you completed: "))
            for i, task in enumerate(tasks, start=1):
                if i == done:
                    task['done'] = True
                    print("Task marked complete!")
                    break
        except ValueError:
            print("Invalid input. Please enter a number.")


while True:
    print("=== To-Do List with Deadlines ===")
    print("1) Add task")
    print("2) View tasks")
    print("3) Complete task")
    print("4) Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        view_task()
    elif choice == "3":
        complete_task()
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid input.")










































































