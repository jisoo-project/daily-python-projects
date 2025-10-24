import datetime

books_file = "books.txt"

def add_book():
    title = input("Title: ").strip()
    author = input("Author: ").strip()

    if not title or not author:
        print("Title or Author cannot be empty.")
        return

    with open(books_file, "a") as f:
        f.write(f"{title} | {author} | available | | \n")
    print("Saved!")

def list_books():
    try:
        with open(books_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No books yet.")
        return
    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

def borrow_book():
    try:
        with open(books_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No books yet.")
        return
    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

    try:
        number = int(input("Which number to borrow?: ").strip())
    except ValueError:
        print("Please enter a number.")
        return
    if number <= 0 or len(lines) < number:
        print("Invalid number.")
        return

    name = input("Borrower name: ").strip()
    if not name:
        print("Borrower name cannot be empty.")
        return

    due = input("Due date (YYYY-MM-DD): ").strip()

    idx = number - 1
    parts = [p.strip() for p in lines[idx].split("|")]
    if len(parts) < 5:
        print("Malformed line; cannot borrow.")
        return

    title, author, status, borrower, due_date = parts[:5]

    if status.lower() != "available":
        print("This book is not available.")
        return

    try:
        datetime.date.fromisoformat(due)
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    status = "loaned"
    borrower = name
    due_date = due

    lines[idx] = f"{title} | {author} | {status} | {borrower} | {due_date}"

    with open(books_file, "w") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))

    print("Borrowed!")

def return_book():
    try:
        with open(books_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No books yet.")
        return
    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

    try:
        number = int(input("Which number to return?: ").strip())
    except ValueError:
        print("Please enter a number.")
        return

    if number <= 0 or len(lines) < number:
        print("Invalid number.")
        return

    idx = number - 1
    parts = [p.strip() for p in lines[idx].split("|")]
    if len(parts) < 5:
        print("Malformed line; cannot return.")
        return

    title, author, status, borrower, due_date = parts[:5]

    if status.lower() != "loaned":
        print("This book is not loaned.")
        return

    status = "available"
    borrower = ""
    due_date = ""

    lines[idx] = f"{title} | {author} | {status} | {borrower} | {due_date}"

    with open(books_file, "w") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))

    print("Returned!")

def search_books():
    try:
        with open(books_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No books yet.")
        return

    query = input("Search text (matches title or author): ").strip()
    text = query.lower()

    matches = []
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 2:
            continue
        title, author = parts[:2]
        if any(text in field.lower() for field in (title, author)):
            matches.append(line)

    if not matches:
        print("No matches.")
    else:
        print(f"=== Results for '{query}' ===")
        for i, match in enumerate(matches, start=1):
            print(f"{i}. {match}")

def show_overdue():
    try:
        with open(books_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No books yet.")
        return

    today = datetime.date.today()

    overdue = []
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == 5:
            status = parts[2].lower()
            if status != "loaned":
                continue
            due_date_text = parts[4]
            if not due_date_text:
                continue
            try:
                due_date = datetime.date.fromisoformat(due_date_text)
            except ValueError:
                continue
            if due_date < today:
                overdue.append(line)

    if not overdue:
        print("No overdue books.")
    else:
        print("=== Overdue ===")
        for i, line in enumerate(overdue, start=1):
            print(f"{i}. {line}")

while True:
    print("=== Library Loan Tracker ===")
    print("1) Add book")
    print("2) List books")
    print("3) Borrow a book")
    print("4) Return a book")
    print("5) Search (by title/author)")
    print("6) Show overdue books")
    print("7) Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        list_books()
    elif choice == "3":
        borrow_book()
    elif choice == "4":
        return_book()
    elif choice == "5":
        search_books()
    elif choice == "6":
        show_overdue()
    elif choice == "7":
        print("Goodbye!")
        break
    else:
        print("Invalid input.")