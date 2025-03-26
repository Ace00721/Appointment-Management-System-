import hashlib
import sqlite3

class AuthManager:
    def __init__(self, db_name="business.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_users_table()

    def create_users_table(self):
        """Creates the users table with role differentiation."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT CHECK(role IN ('admin', 'client')) NOT NULL
            )
        ''')
        self.conn.commit()

    def hash_password(self, password):
        """Hashes a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password, role):
        """Registers a new user as either 'admin' or 'client'."""
        hashed_password = self.hash_password(password)
        try:
            self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
            self.conn.commit()
            print(f"{role.capitalize()} account created successfully!")
        except sqlite3.IntegrityError:
            print("Error: Username already exists. Choose another one.")

    def login(self, username, password):
        """Logs in a user and returns their role."""
        hashed_password = self.hash_password(password)
        self.cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = self.cursor.fetchone()
        if user:
            role = user[0]
            print(f"Login successful! Welcome, {username} ({role.capitalize()})")
            return role  # Return role for access control
        else:
            print("Invalid username or password.")
            return None  # Login failed

    def close(self):
        """Closes the database connection."""
        self.conn.close()

# Run the authentication system
if __name__ == "__main__":
    auth = AuthManager()

    while True:
        choice = input("Do you want to register (r) or login (l)? (q to quit): ")
        if choice == 'r':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            role = input("Enter account type ('admin' or 'client'): ").lower()
            if role not in ["admin", "client"]:
                print("Invalid role. Please enter 'admin' or 'client'.")
            else:
                auth.register(username, password, role)
        elif choice == 'l':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            role = auth.login(username, password)
            if role == "admin":
                print("Access granted! You have admin privileges.")
                # Call admin dashboard or functionalities here
            elif role == "client":
                print("Access granted! You have client privileges.")
                # Call client dashboard or functionalities here
        elif choice == 'q':
            break
        else:
            print("Invalid choice. Please enter 'r', 'l', or 'q'.")

    auth.close()
