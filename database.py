import sqlite3

class DatabaseManager:
    def __init__(self, db_name="business.db"):
        """Initialize database connection and create tables."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates tables for Admins, Clients, Payments, and Appointments."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_info TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_info TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
        """)

        self.conn.commit()

    def add_admin(self, name, contact_info):
        """Adds an admin to the database."""
        self.cursor.execute("INSERT INTO admins (name, contact_info) VALUES (?, ?)", (name, contact_info))
        self.conn.commit()

    def add_client(self, name, contact_info):
        """Adds a client to the database."""
        self.cursor.execute("INSERT INTO clients (name, contact_info) VALUES (?, ?)", (name, contact_info))
        self.conn.commit()

    def add_payment(self, client_id, amount, date):
        """Adds a payment record for a client."""
        self.cursor.execute("INSERT INTO payments (client_id, amount, date) VALUES (?, ?, ?)", (client_id, amount, date))
        self.conn.commit()

    def add_appointment(self, client_id, date, time):
        """Adds an appointment for a client."""
        self.cursor.execute("INSERT INTO appointments (client_id, date, time) VALUES (?, ?, ?)", (client_id, date, time))
        self.conn.commit()

    def get_clients(self):
        """Retrieves all clients."""
        self.cursor.execute("SELECT * FROM clients")
        return self.cursor.fetchall()

    def get_payments(self):
        """Retrieves all payments."""
        self.cursor.execute("SELECT * FROM payments")
        return self.cursor.fetchall()

    def get_appointments(self):
        """Retrieves all appointments."""
        self.cursor.execute("SELECT * FROM appointments")
        return self.cursor.fetchall()

    def get_client_payments(self, client_id):
        """Retrieves payments for a specific client."""
        self.cursor.execute("SELECT * FROM payments WHERE client_id = ?", (client_id,))
        return self.cursor.fetchall()

    def get_client_appointments(self, client_id):
        """Retrieves appointments for a specific client."""
        self.cursor.execute("SELECT * FROM appointments WHERE client_id = ?", (client_id,))
        return self.cursor.fetchall()

    def close(self):
        """Closes the database connection."""
        self.conn.close()


# # Example Usage
# if __name__ == "__main__":
#     db = DatabaseManager()
#
#     # Adding example data
#     db.add_admin("John Doe", "johndoe@example.com")
#     db.add_client("Client A", "clienta@example.com")
#
#     # Fetch client ID (assuming Client A was the first client added)
#     clients = db.get_clients()
#     client_id = clients[0][0]  # First client ID
#
#     db.add_payment(client_id, 500.0, "03-19")
#     db.add_appointment(client_id, "03-21", "10:00 AM")
#
#     print("Clients:", db.get_clients())
#     print("Payments:", db.get_payments())
#     print("Appointments:", db.get_appointments())
#
#     db.close()
