import hashlib

# Dictionary to store user credentials (for demo purposes, use a database in production)
users = {}

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    username = input("Enter a username: ")
    if username in users:
        print("Username already exists. Choose another one.")
        return
    password = input("Enter a password: ")
    users[username] = hash_password(password)
    print("User registered successfully!")

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in users and users[username] == hash_password(password):
        print("Login successful!")
    else:
        print("Invalid username or password.")

while True:
    choice = input("Do you want to register (r) or login (l)? (q to quit): ")
    if choice == 'r':
        register()
    elif choice == 'l':
        login()
    elif choice == 'q':
        break
    else:
        print("Invalid choice. Please enter 'r', 'l', or 'q'.")
