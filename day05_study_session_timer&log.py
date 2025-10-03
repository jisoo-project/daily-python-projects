import time
import datetime

file_path = "sessions.txt"

def start_session():
    topic = input("Topic?: ").strip() or "general"
    try:
        minutes = float(input("Minutes?: ").strip())
        if minutes <= 0:
            print("Please enter minutes > 0.")
            return
    except ValueError:
        print("Please enter a valid number for minutes.")
        return
    print(f"... (waits {minutes} minutes) ...")
    time.sleep(minutes*60)
    print("✅ Session complete!")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a") as file:
        file.write(f"{now} | topic={topic} | minutes={minutes:.2f}\n")
        print("(saved to sessions.txt)")

def view_history():
    with open(file_path, "r") as file:
        lines = file.readlines()

        if not lines:
            print("No sessions yet.")
            return

        print("=== History ===")
        for i, line in enumerate(lines, start=1):
            print(f"{i}. {line.strip()}")

def show_total_min():
    with open(file_path, "r") as file:
        lines = file.readlines()
        if not lines:
            print("No sessions yet.")
            return
        total = 0
        for line in lines:
            parts = line.split("|")
            minutes_text = parts[-1].strip()
            number = minutes_text.replace("minutes=", "")
            minutes = float(number)
            total += minutes
        print(f"Total minutes studied: {total:.2f} minutes")



while True:
    print("=== Study Session Timer ===")
    print("1) Start a session")
    print("2) View history")
    print("3) Show total minutes")
    print("4) Exit")

    choice = input("Choose: ")

    if choice == "1":
        start_session()
    elif choice == "2":
        view_history()
    elif choice == "3":
        show_total_min()
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid input.")











































































