import datetime
import random

rolls_file = "rolls.txt"

def simulate_rolls():
    try:
        n = int(input("How many rolls?: ").strip())
    except ValueError:
        print("Please enter a number.")
        return

    if n <= 0:
        print("It cannot be below or equal to zero.")
        return

    if n > 1_000_000:
        print("Let's keep it under a million rolls 😊")
        return

    counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
    for _ in range(n):
        roll = random.randint(1,6)
        counts[roll] += 1

    total = sum(counts.values())
    print(f"{'Face':<6}{'Count':<8}{'Percent'}")
    for face in sorted(counts):
        count = counts[face]
        percent = (count/total) * 100
        print(f"{face:<6}{count:<8}{percent:.1f}%")

    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    counts_result = ", ".join(f"{face}:{count}" for face, count in counts.items())
    with open(rolls_file, "a") as f:
        f.write(f"{today} | rolls={n} | counts={counts_result}\n")
    print("Saved to rolls.txt")

def view_history():
    try:
        with open(rolls_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No history yet.")
        return

    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

def show_stats():
    try:
        with open(rolls_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No history yet.")
        return

    total = len(lines)
    rolls_list = []
    counts_dict = {}

    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        time, rolls, counts = parts[:3]
        roll_parts = rolls.split("=")
        if len(roll_parts) != 2:
            continue
        try:
            rolls_list.append(int(roll_parts[1].strip()))
        except ValueError:
            continue
        counts = counts.replace("counts=", "").strip()
        for pair in counts.split(","):
            pair = pair.strip()
            if ":" not in pair:
                continue
            face_text, count_text = pair.split(":", 1)
            try:
                face = int(face_text.strip())
                cnt = int(count_text.strip())
            except ValueError:
                continue

            counts_dict[face] = counts_dict.get(face, 0) + cnt


    highest_value = max(counts_dict.values())
    highest_key = max(counts_dict, key=counts_dict.get)
    total_rolls = sum(rolls_list)

    print("=== Stats ===")
    print(f"Total sessions: {total}")
    print(f"Total rolls: {total_rolls}")
    print(f"Average rolls per session: {total_rolls/total:.2f}")
    print(f"Most common face overall: {highest_key} (count={highest_value})")

def main():
    while True:
        print("=== Dice Roll Analyzer ===")
        print("1) Simulate rolls")
        print("2) View history")
        print("3) Show stats")
        print("4) Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            simulate_rolls()
        elif choice == "2":
            view_history()
        elif choice == "3":
            show_stats()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid input.")

if __name__ == "__main__":
    main()











