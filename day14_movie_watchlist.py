movies_file = "movies.txt"

def add_movie():
    title = input("Title: ").strip()
    try:
        year = int(input("Year (YYYY): ").strip())
    except ValueError:
        print("Please enter a number.")
        return
    genres = input("Genres (comma-separated): ").strip()

    if not title or not year:
        print("Title and Year cannot be empty.")
        return

    if len(str(year)) != 4:
        print("Year has to be 4-digit number.")
        return

    with open(movies_file, "a") as f:
        f.write(f"{title} | {year} | {genres} | todo | - \n")
    print("Saved!")

def list_movies():
    try:
        with open(movies_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No movies yet.")
        return

    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

def search_movies():
    try:
        with open(movies_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No movies yet.")
        return

    query = input("Search text (title or genre): ").strip()
    text = query.lower()

    matches = []
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        title, year, genres = parts[:3]
        matched = False
        for g in genres.split(","):
            tag = g.strip().lower()
            if text in title.lower() or text in tag.lower():
                matched = True
                break
        if matched:
            matches.append(line)

    if not matches:
        print("No matches.")
    else:
        print(f'=== Results for "{query}" ===')
        for i, match in enumerate(matches, start=1):
            print(f"{i}. {match}")

def mark_watched():
    try:
        with open(movies_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No movies yet.")
        return

    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

    try:
        number = int(input("Which number to mark as watched: "))
    except ValueError:
        print("Please enter a number.")
        return

    if number <= 0 or number > len(lines):
        print("Invalid number.")
        return

    idx = number - 1
    parts = [p.strip() for p in lines[idx].split("|")]
    title, year, genres, status, rating = parts[:5]
    if status.lower() == "watched":
        print("Already watched.")
        return
    else:
        status = "watched"

    lines[idx] = f"{title} | {year} | {genres} | {status} | {rating}"

    with open(movies_file, "w") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))
    print("Marked as watched.")

def rate_movie():
    try:
        with open(movies_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No movies yet.")
        return

    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

    try:
        number = int(input("Which number to rate?: ").strip())
    except ValueError:
        print("Please enter a number.")
        return

    if number <= 0 or number > len(lines):
        print("Invalid number.")
        return

    try:
        rating = float(input("Rating (0-10): ").strip())
    except ValueError:
        print("Please enter a number.")
        return

    if rating < 0 or rating > 10:
        print("Invalid number.")
        return

    idx = number - 1
    parts = [p.strip() for p in lines[idx].split("|")]
    title, year, genres, status, rate = parts[:5]

    rate = f"{rating:.1f}"

    lines[idx] = f"{title} | {year} | {genres} | {status} | {rate}"

    with open(movies_file, "w") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))
    print("Rated!")

def show_stats():
    try:
        with open(movies_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No movies yet.")
        return

    total = len(lines)
    watched = 0
    to_watch = 0
    genres_dict = {}
    ratings = []
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 5:
            continue
        title, year, genres, status, rate = parts[:5]

        if status.lower() != "watched":
            to_watch += 1
        else:
            watched += 1

        for g in genres.split(","):
            tag = g.strip().lower()
            if not tag:
                continue
            genres_dict[tag] = genres_dict.get(tag, 0) + 1

        if rate and rate != "-":
            try:
                ratings.append(float(rate))
            except ValueError:
                pass

    average_rating = sum(ratings) / len(ratings) if ratings else None

    print("=== Stats ===")
    print(f"Total: {total} | Watched: {watched} | To watch: {to_watch}")
    print(f"Average rating: {average_rating:.2f}" if average_rating is not None else "Average rating: N/A")

    if genres_dict:
        by_genre = ", ".join(f"{k}={v}" for k, v in sorted(genres_dict.items()))
        print("By genre: ", by_genre)
    else:
        print("By genre: N/A")

def delete_movie():
    try:
        with open(movies_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No movies yet.")
        return

    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

    try:
        number = int(input("Which number to delete?: ").strip())
    except ValueError:
        print("Please enter a number.")
        return

    if number <= 0 or number > len(lines):
        print("Invalid number.")
        return

    del lines[number-1]
    with open(movies_file, "w") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))
    print("Deleted.")

while True:
    print("=== Movie Watchlist ===")
    print("1) Add movie")
    print("2) List movies")
    print("3) Search (by title or genre)")
    print("4) Mark as watched")
    print("5) Rate a movie")
    print("6) Show stats")
    print("7) Delete movie")
    print("8) Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_movie()
    elif choice == "2":
        list_movies()
    elif choice == "3":
        search_movies()
    elif choice == "4":
        mark_watched()
    elif choice == "5":
        rate_movie()
    elif choice == "6":
        show_stats()
    elif choice == "7":
        delete_movie()
    elif choice == "8":
        print("Goodbye!")
        break
    else:
        print("Invalid input.")