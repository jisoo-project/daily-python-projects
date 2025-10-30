import datetime

books_file = "books.txt"
logs_file = "logs.txt"

def add_book():
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    try:
        total_pages = int(input("Total pages: ").strip())
    except ValueError:
        print("Please enter a number.")
        return

    if total_pages <= 0:
        print("Pages cannot be below or equal to zero.")
        return

    if not title or not author:
        print("You cannot leave title/author empty.")
        return

    with open(books_file, "a") as f:
        f.write(f"{title} | {author} | {total_pages} | todo\n")
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

def log_reading():
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
        number = int(input("Which book number?: ").strip())
    except ValueError:
        print("Please enter a number.")
        return

    if number <= 0 or len(lines) < number:
        print("Invalid number.")
        return

    selected_line = lines[number-1]
    parts = [p.strip() for p in selected_line.split("|")]
    title, author, total_pages, status = parts[:4]

    try:
        pages = int(input("Pages read today: ").strip())
    except ValueError:
        print("Please enter a number.")
        return

    if pages < 0 or pages > int(total_pages):
        print("Invalid number.")
        return

    if status == "todo":
        status = "reading"
        lines[number-1] = f"{title} | {author} | {total_pages} | {status}"
        with open(books_file, "w") as f:
            f.write("\n".join(lines) + ("\n" if lines else ""))

    with open(logs_file, "a") as f:
        f.write(f"{datetime.date.today()} | title={title} | pages={pages}\n")

    print("Saved!")

def view_reading():
    try:
        with open(logs_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No logs yet.")
        return

    matches = []
    for i, line in enumerate(lines, start=1):
        parts = [p.strip() for p in line.split("|")]
        if parts[0] == datetime.date.today().isoformat():
            matches.append(line)

    if not matches:
        print("No reading logged today.")
    else:
        for i, match in enumerate(matches, start=1):
            print(f"{i}. {match}")

def show_stats():
    books_map = {}

    try:
        with open(books_file, "r") as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                parts = [p.strip() for p in ln.split("|")]
                if len(parts) < 3:
                    continue
                title, author, total_pages = parts[:3]
                books_map[title] = int(total_pages)
    except FileNotFoundError:
        books_map = {}

    title_pages = {}
    dates = set()
    try:
        with open(logs_file, "r") as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                parts = [p.strip() for p in ln.split("|")]
                if len(parts) < 3:
                    continue
                date_text = parts[0]
                t_field = parts[1]
                p_field = parts[2]

                if not t_field.startswith("title=") or not p_field.startswith("pages="):
                    continue

                title = t_field.split("=", 1)[1].strip()
                try:
                    pages = int(p_field.split("=", 1)[1])
                except ValueError:
                    continue

                title_pages[title] = title_pages.get(title, 0) + pages
                dates.add(date_text)

    except FileNotFoundError:
        pass

    total_books = len(books_map)
    total_pages_read = sum(title_pages.values())
    average_pages = total_pages_read/len(dates)

    print("=== Stats ===")
    for title, total_p in books_map.items():
        read = title_pages.get(title, 0)
        pct = (read/total_p) * 100 if total_p else 0
        remaining = max(total_p - read, 0)
        print(f"{title}: {read}/{total_p} ({pct:.1f}%) remaining={remaining}")

    print("---")
    print(f"Total books: {total_books}")
    print(f"Total pages read: {total_pages_read}")
    print(f"Average pages/day: {average_pages}")

def finished():
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
        number = int(input("Which book number?: ").strip())
    except ValueError:
        print("Please enter a number.")
        return

    if number <= 0 or len(lines) < number:
        print("Invalid number.")
        return

    selected_line = lines[number - 1]
    parts = [p.strip() for p in selected_line.split("|")]
    title, author, total_pages, status = parts[:4]

    if status.lower() == "reading":
        status = "finished"
        lines[number-1] = f"{title} | {author} | {total_pages} | {status}"
        with open(books_file, "w") as f:
            f.write("\n".join(lines) + ("\n" if lines else ""))
        print("Changed to 'finished'")
        return
    elif status.lower() == "finished":
        print("It is already finished.")
        return
    else:
        print("You can only finish reading books.")
        return

while True:
    print("=== Reading Progress Tracker ===")
    print("1) Add book")
    print("2) List books")
    print("3) Log reading (pages today)")
    print("4) View today’s reading")
    print("5) Show stats (per book + overall)")
    print("6) Mark book as finished")
    print("7) Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        list_books()
    elif choice == "3":
        log_reading()
    elif choice == "4":
        view_reading()
    elif choice == "5":
        show_stats()
    elif choice == "6":
        finished()
    elif choice == "7":
        print("Goodbye!")
        break
    else:
        print("Invalid input.")










