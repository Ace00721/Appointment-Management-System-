import hashlib
import sqlite3

class AuthManager:
    def __init__(self, db_name="business.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_users_table()

    def create_users_table(self):
        """Creates the users table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        self.conn.commit()

    def hash_password(self, password):
        """Hashes a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        """Registers a new user."""
        hashed_password = self.hash_password(password)
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            self.conn.commit()
            print("User registered successfully!")
        except sqlite3.IntegrityError:
            print("Error: Username already exists. Choose another one.")

    def login(self, username, password):
        """Logs in a user by checking hashed password."""
        hashed_password = self.hash_password(password)
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = self.cursor.fetchone()
        if user:
            print("Login successful! Welcome,", username)
            return True  # Login success
        else:
            print("Invalid username or password.")
            return False  # Login failed

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
            auth.register(username, password)
        elif choice == 'l':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if auth.login(username, password):
                print("Access granted!")
                break  # Exit loop after successful login
        elif choice == 'q':
            break
        else:
            print("Invalid choice. Please enter 'r', 'l', or 'q'.")

    auth.close()
