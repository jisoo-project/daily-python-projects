import datetime
import random

cards_file = "cards.txt"
stats_file = "stats.txt"
missed_cards = []

def add_card():
    term = input("Term: ").lower()
    definition = input("Definition: ").lower()

    if not term:
        print("You cannot leave the term empty.")
        return

    if not definition:
        print("You cannot leave the definition empty.")
        return
    if "|" in term or "|" in definition:
        print("Please don't use the '|' character.")
        return

    with open(cards_file, "a") as f:
        f.write(f"{term} | {definition}\n")
        print("Saved!")

def list_cards():
    try:
        with open(cards_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No cards yet.")
        return

    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

def quiz_me():
    global missed_cards

    try:
        with open(cards_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No cards yet.")
        return

    cards = []
    for line in lines:
        line = line.strip()
        parts = line.split("|")
        term = parts[0].lower()
        definition = parts[1].lower()
        if len(parts) != 2:
            continue
        card_tuple = (term,definition)
        cards.append(card_tuple)

    try:
        practice = int(input("How many cards you want to practice?: "))
    except ValueError:
        print("It has to be an integer.")
        return

    if practice <= 0:
        print("Choose a positive number.")
        return

    if practice > len(cards):
        print("It cannot be over the number of cards!")
        return

    selected = random.sample(cards, practice)

    total = practice
    correct = 0
    missed = 0

    for i, card in enumerate(selected, start=1):
        print(f"Q{i}) Term: {card[0]}")
        answer = input("Your answer: ").lower().strip()
        if answer == card[1].strip().lower():
            print("✅ Correct!")
            correct += 1
        else:
            print(f"❌ Wrong. Expected: {card[1]}")
            missed += 1
            missed_cards.append((card[0],card[1]))

    today = datetime.datetime.today()
    now = today.strftime("%Y-%m-%d %H:%M:%S")
    with open(stats_file, "a") as f:
        f.write(f"{now} | total={total} | correct={correct}\n")
    print(f"Score: {correct}/{total}")
    print("Saved to stats.")

def review_missed():
    if not missed_cards:
        print("No missed cards from the last quiz.")
        return

    print("=== Missed Cards (last quiz) ===")
    for card in missed_cards:
        print(f"{card[0]} - > {card[1]}")

def show_stats():
    try:
        with open(stats_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No stats yet.")
        return

    scores = []

    print("=== Recent Sessions ===")
    for i, line in enumerate(lines, start=1):
        parts = line.split("|")
        total = int(parts[1].split('=')[1])
        correct = int(parts[2].split('=')[1])
        print(f"{i}. {line}")
        score = (int(correct)/int(total)) * 100
        scores.append(score)

    total = 0
    for score in scores:
        total += score


    print(f"Total sessions: {len(lines)}")

    print(f"Best score: {max(scores):.1f}%")
    print(f"Average accuracy: {total/len(scores):.1f}%")

while True:
    print("=== Flashcard Quizzer ===")
    print("1) Add card")
    print("2) List cards")
    print("3) Quiz me")
    print("4) Review missed (last quiz)")
    print("5) Show stats")
    print("6) Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_card()
    elif choice == "2":
        list_cards()
    elif choice == "3":
        quiz_me()
    elif choice == "4":
        review_missed()
    elif choice == "5":
        show_stats()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid input.")