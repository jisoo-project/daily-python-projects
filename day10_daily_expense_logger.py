import datetime

expense_file = "expenses.txt"

def add_expense():
    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            print("Amount cannot be below or equal to zero.")
            return
    except ValueError:
        print("Please enter a valid number for amount.")

    category = input("Category: ")
    note = input("Note (Optional): ")

    if not note:
        note = " "

    if not category:
        print("You cannot leave the category empty.")
        return

    with open(expense_file, "a") as f:
        f.write(f"{datetime.date.today()} | {amount:.2f} | {category} | {note}\n")
    print("Saved!")

def view_today():
    try:
        with open(expense_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No expenses yet.")
        return

    today = []
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 4:
            continue
        date = parts[0].strip()
        if date == str(datetime.date.today()):
            today.append(line)

    if not today:
        print("There is no today's expense.")
        return

    print("=== Today's Expense ===")
    for i, expense in enumerate(today, start=1):
        print(f"{i}. {expense}")

def weekly_summary():
    one_week = datetime.timedelta(weeks=1)

    try:
        with open(expense_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No expenses yet.")
        return

    expenses = []
    today = datetime.date.today()
    start_date = datetime.date.today() - one_week
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 4:
            continue
        date = parts[0].strip()
        expense = parts[1].strip()
        expense = float(expense)
        date_object = datetime.date.fromisoformat(date)
        if start_date <= date_object <= today:
            expenses.append(expense)

    total = 0
    for expense in expenses:
        total += expense
    print("=== Weekly Summary ===")
    print(f"Total this week: {total:.2f}")
    print(f"Average per day: {total/7:.2f}")



while True:
    print("=== Daily Expense Logger ===")
    print("1) Add new expense")
    print("2) View today's expenses")
    print("3) View weekly summary")
    print("4) Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_today()
    elif choice == "3":
        weekly_summary()
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid input.")
