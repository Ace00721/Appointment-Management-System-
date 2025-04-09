accounts = {}  # stores accounts: {username: {password, email, phone}}

def create_account():
    print("Create a New Account")
    username = input("Enter a username: ").strip()

    if username in accounts:
        print("Username already exists.")
        return

    email = input("Enter your email: ").strip()
    phone = input("Enter your phone number: ").strip()

    # checks for duplicate email or phone
    for user_info in accounts.values():
        if user_info["email"] == email:
            print(" This email is already in use.")
            return
        if user_info["phone"] == phone:
            print("This phone number is already in use.")
            return

    password = input("Enter a password: ")
    confirm = input("Confirm your password: ")

    if password != confirm:
        print("Passwords do not match.")
        return

    # saves account
    accounts[username] = {
        "password": password,
        "email": email,
        "phone": phone
    }

    print(f" Account for '{username}' created successfully!")
def view_accounts():  # For testing/demo only
    print("\n Current Accounts:")
    for user, info in accounts.items():
        print(f" - {user}: {info}")
    print()

while True:
    print("\n1. Create Account\n2. View Accounts (demo)\n3. Exit")
    choice = input("Choose an option: ")

    if choice == '1':
        create_account()
    elif choice == '2':
        view_accounts()
    elif choice == '3':
        break
    else:
        print("Invalid choice. Try again.")




