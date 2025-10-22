import datetime

bookmark_file = "bookmarks.txt"

def add_bookmark():
    title = input("Title: ")
    url = input("URL: ")
    tags = input("Tags (comma-separated, optional) : ")

    if not title or not url:
        print("You cannot leave title or url empty.")
        return

    tags = tags or " "

    with open(bookmark_file, "a") as f:
        f.write(f"{title} | {url} | {tags} | {datetime.date.today()}\n")
    print("Saved!")

def list_bookmarks():
    try:
        with open(bookmark_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No bookmarks yet.")
        return

    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

def search_bookmarks():
    try:
        with open(bookmark_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No bookmarks yet.")
        return

    query = input("Search text (matches title, url, or tags): ").strip()
    text = query.lower()

    matches = []
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        title, url, tags = parts[:3]
        if any(text in field.lower() for field in (title, url, tags)):
            matches.append(line)

    if not matches:
        print("No matches")
    else:
        print(f"=== Results for '{query}' ===")
        for i, match in enumerate(matches, start=1):
            print(f"{i}. {match}")

def delete_bookmark():
    try:
        with open(bookmark_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No bookmarks yet.")
        return

    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

    try:
        number = int(input("Which number to delete?: "))
    except ValueError:
        print("Please enter a number.")
        return

    if number <= 0 or number > len(lines):
        print("Invalid number.")
        return

    del lines[number - 1]

    with open(bookmark_file, "w") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))
    print("Deleted!")

def show_stats():
    try:
        with open(bookmark_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No bookmarks yet.")
        return

    total = len(lines)

    dates = []
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4:
            try:
                dates.append(datetime.date.fromisoformat(parts[3]))
            except ValueError:
                pass
    newest = max(dates).isoformat() if dates else "N/A"

    tags_counts = {}
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        tag_text = parts[2]
        tags_list = [t.strip().lower() for t in tag_text.split(",")]
        for tag in tags_list:
            if tag in tags_counts:
                tags_counts[tag] += 1
            else:
                tags_counts[tag] = 1

    print("=== Stats ===")
    print(f"Total: {total}")
    print("By tag:", end= " ")
    print(", ".join(f"{key}={value}" for key, value in tags_counts.items()))
    print(f"Newest: {newest}")

while True:
    print("=== Bookmark Saver ===")
    print("1) Add bookmark")
    print("2) List bookmarks")
    print("3) Search (by keyword or tag)")
    print("4) Delete bookmark (by number)")
    print("5) Show stats")
    print("6) Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_bookmark()
    elif choice == "2":
        list_bookmarks()
    elif choice == "3":
        search_bookmarks()
    elif choice == "4":
        delete_bookmark()
    elif choice == "5":
        show_stats()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid input.")

