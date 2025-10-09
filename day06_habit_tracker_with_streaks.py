import datetime

habits = "habits.txt"
checkins = "checkins.txt"

def add_habit():
    habit_name = input("What habit do you want to track?: ").strip()
    if habit_name == "":
        print("Please enter a habit name: ")
        return

    try:
        with open(habits, "r") as f:
            existing = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        existing = []

    if any(h.lower() == habit_name.lower() for h in existing):
        print("Duplicate name.")
        return

    with open(habits, "a") as f:
        f.write(habit_name+"\n")
    print("Habit saved!")

def list_habits():
    try:
        with open(habits, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No habits yet.")
        return

    for i, habit in enumerate(lines, start=1):
        print(f"{i}. {habit}")

def check_in():
    try:
        with open(habits, "r") as file:
            habit_list = [ln.strip() for ln in file if ln.strip()]
    except FileNotFoundError:
        habit_list = []

    if not habit_list:
        print("No habits yet.")
        return

    for i, h in enumerate(habit_list, start=1):
        print(f"{i}. {h}")

    try:
        n = int(input("Which habit number do you want to check in for?: "))
        if n < 1 or n>len(habit_list):
            print("Invalid number.")
            return
    except ValueError:
        print("Please enter a number.")
        return

    habit_name = habit_list[n-1]
    today = datetime.date.today().isoformat()

    try:
        with open(checkins, "r") as file:
            check_lines = [ln.strip() for ln in file if ln.strip()]
    except FileNotFoundError:
        check_lines = []

    target = f"{today} | {habit_name}"
    if any(ln == target for ln in check_lines):
        print("Already checked in today for this habit.")
        return

    with open(checkins, "a") as file:
        file.write(target + "\n")
    print("Checked in!")

def view_streaks():
    try:
        with open(checkins, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No check-ins yet.")
        return

    dictionary = {}
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 2:
            continue
        date_text, habit = parts
        try:
            d = datetime.date.fromisoformat(date_text)
        except ValueError:
            continue
        dictionary.setdefault(habit,[]).append(d)

    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)

    print("=== Current Streaks ===")
    for habit,dates in dictionary.items():
        dates_set = set(dates)
        streak = 0
        curr = today
        while curr in dates_set:
            streak += 1
            curr -= one_day
        print(f"{habit} - current streak: {streak} day(s)")

def view_checkin_history():
    try:
        with open(checkins, "r") as file:
            lines = [ln.strip() for ln in file if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No check-ins yet.")
        return
    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")


while True:
    print("=== Habit Tracker ===")
    print("1) Add habit")
    print("2) List habits")
    print("3) Check in (mark today done)")
    print("4) View streaks")
    print("5) View check-in history")
    print("6) Exit")

    choice = input("Enter: ")

    if choice == "1":
        add_habit()
    elif choice == "2":
        list_habits()
    elif choice == "3":
        check_in()
    elif choice == "4":
        view_streaks()
    elif choice == "5":
        view_checkin_history()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid input")