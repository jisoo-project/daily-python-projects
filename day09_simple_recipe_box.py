
recipes_file = "recipes.txt"

def add_recipe():
    title = input("Title: ").strip()
    ingredients = input("Ingredients (comma-separated): ").strip()
    time = int(input("Time in minutes: ").strip())
    notes = input("Notes (optional): ").strip()

    if not notes:
        notes = " "

    if not title or not ingredients or not time:
        print("You cannot leave title | ingredients | time empty.")
        return

    if time <= 0:
        print("Time cannot be below or equals to zero.")
        return

    if "|" in title or "|" in ingredients or "|" in notes:
        print("Please don't use 'l' character")
        return

    with open(recipes_file, "a") as f:
        f.write(f"{title} | {ingredients} | {time} | {notes}\n")
        print("Saved!")

def list_recipes():
    try:
        with open(recipes_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No recipes yet.")
        return

    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

def search_by_ingredients():
    ingredient = input("Ingredient to search: ").lower().strip()

    try:
        with open(recipes_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No recipes to search.")
        return


    matches = []
    for line in lines:
        parts = line.split("|")
        ingredients_text = parts[1] if len(parts) > 1 else ""
        ingredients_list = [x.strip().lower() for x in ingredients_text.split(",") if x.strip()]
        for ing in ingredients_list:
            if ing.lower() == ingredient:
               matches.append(line)

    print(f'=== Results for "{ingredient}"===')

    if matches:
        for i, line in enumerate(matches, start=1):
            print(f"{i}. {line}")
    else:
        print("No recipes match that ingredient.")

def show_quick_recipes():
    try:
        with open(recipes_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No recipes yet.")
        return

    try:
        minutes = int(input("Max minutes?: ").strip())
    except ValueError:
        print("Please enter a whole number.")
        return

    if minutes <= 0:
        print("It cannot be below or equal to zero.")
        return

    matches = []
    for line in lines:
        parts = line.split("|")
        minutes_value = parts[2].strip()
        if int(minutes_value) <= minutes:
            matches.append(line)

    if not matches:
        print("No recipes under that time.")
    else:
        print(f"=== Quick recipes (<={minutes} min)")
        for i, line in enumerate(matches, start=1):
            print(f"{i}. {line}")

def delete_recipe():
    try:
        with open(recipes_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No recipes yet.")
        return
    for i, line in enumerate(lines, start = 1):
        print(f"{i}. {line}")

    try:
        number = int(input("Which number to delete?: "))
    except ValueError:
        print("Please enter a number.")
        return

    if number < 1 or number > len(lines):
        print("Invalid number.")
    else:
        del lines[number-1]

        with open(recipes_file, "w") as f:
            f.write("\n".join(lines) + ("\n" if lines else ""))

        print("Deleted.")

while True:
    print("=== Recipe Box ===")
    print("1) Add recipe")
    print("2) List recipes")
    print("3) Search by ingredient")
    print("4) Show quick recipes (under N minutes)")
    print("5) Delete a recipe")
    print("6) Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_recipe()
    elif choice == "2":
        list_recipes()
    elif choice == "3":
        search_by_ingredients()
    elif choice == "4":
        show_quick_recipes()
    elif choice == "5":
        delete_recipe()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid input.")