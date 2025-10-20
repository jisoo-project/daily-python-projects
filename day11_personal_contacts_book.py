
contacts_file = "contacts.txt"

def add_contact():
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email (optional) : ").strip()
    note = input("Note (optional) : ").strip()

    if not name or not phone:
        print("You cannot leave name or phone empty.")
        return

    email = email or ""
    note = note or ""

    with open(contacts_file, "a") as f:
        f.write(f"{name} | {phone} | {email} | {note}\n")
    print("Saved!")

def list_contacts():
    try:
        with open(contacts_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No contacts yet.")
        return

    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

def search_contacts():
    try:
        with open(contacts_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No contacts yet.")
        return

    query = input("Search text (name/phone/email) : ").strip()
    text = query.lower()
    matches = []

    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        name,phone,email = parts[:3]
        if any(text in field.lower() for field in (name,phone,email)):
            matches.append(line)

    if not matches:
        print("No matches.")
    else:
        print(f"=== Results for '{query}' ===")
        for i, match in enumerate(matches, start=1):
            print(f"{i}. {match}")

def delete_contact():
    try:
        with open(contacts_file, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        lines = []

    if not lines:
        print("No contacts yet.")
        return

    for i, line in enumerate(lines, start=1):
        print(f"{i}. {line}")

    try:
        num = int(input("Which number to delete?: "))
    except ValueError:
        print("Please enter a number.")
        return

    if num > len(lines) or num <= 0:
        print("Invalid number.")
        return

    del lines[num - 1]

    with open(contacts_file, "w") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))
    print("Deleted!")

while True:
    print("=== Contacts Book ===")
    print("1) Add contact")
    print("2) List contacts")
    print("3) Search contacts (by name/phone/email)")
    print("4) Delete a contact (by number)")
    print("5) Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_contact()
    elif choice == "2":
        list_contacts()
    elif choice == "3":
        search_contacts()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid input.")

