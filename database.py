"""
Database Manager for Appointment and Payment System

This module defines the `DatabaseManager` class, which provides methods for interacting
with a SQLite database that manages clients, admins, payments, and appointments.
"""
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

        # UPDATED appointments table with service, provider, and price
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            service TEXT,
            provider TEXT,
            price REAL,
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

    # UPDATED to accept service, provider, price
    def add_appointment(self, client_id, date, time, service=None, provider=None, price=None):
        """Adds an appointment for a client with optional service details."""
        self.cursor.execute("""
        INSERT INTO appointments (client_id, date, time, service, provider, price)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (client_id, date, time, service, provider, price))
        self.conn.commit()

    def get_appointments(self):
        """Retrieves all appointments with extra details."""
        self.cursor.execute("""
            SELECT date, time, service, provider, price 
            FROM appointments
        """)
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

    def delete_appointment(self, appointment_id):
        """Deletes an appointment by ID."""
        with self.conn:
            self.conn.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))

    def get_clients(self):
        self.cursor.execute("SELECT * FROM clients")
        return self.cursor.fetchall()
