accounts = {}  # store accounts: {username: {password, email, phone}}

def create_account():
    print("Create a New Account")
    username = input("Enter a username: ").strip()

    if username in accounts:
        print("Username already exists.")
        return

    email = input("Enter your email: ").strip()
    phone = input("Enter your phone number: ").strip()

    # check for duplicate email or phone
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

    # Save account
    accounts[username] = {
        "password": password,
        "email": email,
        "phone": phone
    }

    print(f" Account for '{username}' created successfully!")


