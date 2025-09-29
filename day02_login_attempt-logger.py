import datetime
import os

credentials = {
    "admin": "12345",
    "jisoo": "coffee123",
    "guest": "welcome",
    "user": "password"
}

def log_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} Error: {e}")
    return wrapper

@log_error
def login():
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    ok = (username in credentials) and (credentials[username] == password)
    print("✅ Login successful." if ok else "❌ Invalid credentials")

    with open("logins.txt", "a") as f:
        ts = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
        status = "SUCCESS" if ok else "FAIL"
        f.write(f"{ts} | user={username} | {status}\n")

def history():
    path = "logins.txt"
    if not os.path.exists(path):
        print("No attempts yet.")
        return
    with open(path, "r") as f:
        lines = f.readlines()
    if not lines:
        print("No attempts yet.")
    else:
        print("=== Login History ===")
        for line in lines:
            print(line.strip())



while True:
     print("=== Login System ===")
     print("1) Try login")
     print("2) View login history")
     print("3) Exit")

     choice = input("Choose: ")

     if choice == "1":
         login()
     elif choice == "2":
         history()
     elif choice == "3":
         print("Goodbye!")
         break
     else:
         print("Invalid input.")









































































