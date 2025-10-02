import datetime

expenses = []

def add_expense():
    description = input("What did you spend on?: ")
    try:
        amount = float(input("How much did it cost?($): "))
    except ValueError:
        print("Please enter a number: ")
    date = input("When did u spend?(YYYY-MM-DD/Enter by default(Today)): ")
    if not date:
        date = datetime.date.today()
    expenses.append({"description":description, "amount":amount, "date":date})
    print("Expense saved!")

def view_expense():
    if not expenses:
        print("No expense recorded yet.")
    else:
        for i, expense in enumerate(expenses, start=1):
            print(f"{i}. {expense['description']} - ${expense['amount']:.2f} ({expense['date']})")

def show_total():
    total = 0
    if not expenses:
        print("No expense recorded yet.")
    else:
        for expense in expenses:
            total += expense['amount']
        print(f"Total spent: ${total:.2f}")

while True:
    print("=== Expense Tracker ===")
    print("1) Add expense")
    print("2) View expense")
    print("3) Show total")
    print("4) Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expense()
    elif choice == "3":
        show_total()
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid input.")











































































