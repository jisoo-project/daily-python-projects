import string
import datetime

while True:
    print("=== Password Strength Checker ===")

    password = input("Enter a password(exit to escape): ")

    common_passwords = [
        "123456",
        "123456789",
        "qwerty",
        "password",
        "12345",
        "12345678",
        "111111",
        "123123",
        "abc123",
        "1234567",
        "password1",
        "1234",
        "iloveyou",
        "1q2w3e4r",
        "000000",
        "qwerty123",
        "letmein",
        "welcome",
        "dragon",
        "monkey"
    ]


    def log_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error {datetime.datetime.now()} {e}")
        return wrapper

    @log_error
    def check_common():
        found = False
        for n in common_passwords:
            if n == password:
                found = True
                break
        if found:
            print("❌ Weak: Common password.")
        else:
            print("✅ Strong password!")


    @log_error
    def check_length():
        if len(password) >= 15:
            print("✅ Strong password!")
        else:
            print("❌ Weak: Need to be at least 15 characters long.")

    @log_error
    def check_numbers():
        found = False
        for num in password:
            if num.isdigit():
                found = True
                break
        if found:
            print("✅ Strong password!")
        else:
            print("❌ Weak: Needs at least one number.")
    @log_error
    def check_special():
        found = False
        for spe in password:
            if spe in string.punctuation:
                found = True
                break
        if found:
            print("✅ Strong password!")
        else:
            print("❌ Weak: Needs at least one special character.")

    if password.strip() == "":
        print("You didn't enter the password.")
    elif password.lower() == "exit":
        print("Goodbye!")
        break
    else:
        print("Checking common password...")
        check_common()
        print("Checking the length...")
        check_length()
        print("Checking the number...")
        check_numbers()
        print("Checking special character...")
        check_special()






































































