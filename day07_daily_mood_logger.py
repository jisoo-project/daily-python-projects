import datetime

mood_file = "mood.txt"

def log_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
    return wrapper

@log_error
def add_mood():
    mood = input("How are you feeling today? (happy/sad/angry/tired/etc.): ").lower()
    note = input("Any notes you'd like to add? (optional/type 'enter' to skip): ")

    if not note:
        note = " "

    with open(mood_file, "a") as f:
        f.write(f"{datetime.date.today()} | {mood} | {note}\n")
        print("Mood recorded successfully!")

@log_error
def view_mood_history():
    try:
        with open(mood_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No moods recorded yet.")
        return

    print("=== Mood History ===")
    for i, line in enumerate(lines,start=1):
        print(f"{i}. {line}")

@log_error
def mood_summary():
    try:
        with open(mood_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No moods recorded yet.")
        return

    mood_counts = {}

    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 2:
            continue
        mood = parts[1].lower()
        mood_counts[mood] = mood_counts.get(mood, 0) + 1

    print("=== Mood Summary ===")
    for mood, days in mood_counts.items():
        print(f"{mood}: {days} days(s)")


while True:
    print("=== Mood Logger ===")
    print("1) Add a mood")
    print("2) View mood history")
    print("3) View mood summary")
    print("4) Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_mood()
    elif choice == "2":
        view_mood_history()
    elif choice == "3":
        mood_summary()
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid input.")