"""
Unit Tests for Appointment Management System

This module contains unit tests for two key components of the system:
- `DatabaseManager`: Responsible for client, appointment, and payment data.
- `AuthManager`: Handles user registration and authentication.
"""
import unittest
from database import DatabaseManager
from Authentication import AuthManager
import sqlite3

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(db_name=":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_and_get_client(self):
        self.db.add_client("John Doe", "123-456-7890")
        clients = self.db.get_clients()
        self.assertEqual(len(clients), 1)
        self.assertEqual(clients[0][1], "John Doe")

    def test_add_and_get_appointment(self):
        self.db.add_client("Jane Doe", "987-654-3210")
        client_id = self.db.get_clients()[0][0]
        self.db.add_appointment(client_id, "2025-05-01", "10:00", service="Consultation", provider="Dr. Smith", price=150.0)
        appointments = self.db.get_appointments()
        self.assertEqual(len(appointments), 1)
        self.assertEqual(appointments[0][3], "Consultation")

    def test_add_and_get_payment(self):
        self.db.add_client("Jake Doe", "555-555-5555")
        client_id = self.db.get_clients()[0][0]
        self.db.add_payment(client_id, 250.00, "2025-04-28")
        payments = self.db.get_payments()
        self.assertEqual(len(payments), 1)
        self.assertEqual(payments[0][2], 250.00)

    def test_delete_appointment(self):
        self.db.add_client("Jill Doe", "444-444-4444")
        client_id = self.db.get_clients()[0][0]
        self.db.add_appointment(client_id, "2025-06-01", "11:00")
        appointment_id = self.db.get_appointments()[0][0]
        self.db.delete_appointment(appointment_id)
        appointments = self.db.get_appointments()
        self.assertEqual(len(appointments), 0)


class TestAuthManager(unittest.TestCase):
    def setUp(self):
        self.auth = AuthManager(db_name=":memory:")

    def tearDown(self):
        self.auth.close()

    def test_register_and_login_success(self):
        self.auth.register("admin_user", "securepassword", "admin")
        role = self.auth.login("admin_user", "securepassword")
        self.assertEqual(role, "admin")

    def test_register_duplicate_username(self):
        self.auth.register("client_user", "password123", "client")
        # Trying to register the same username should not throw an exception, just a print.
        self.auth.register("client_user", "newpassword", "client")  # Should print error
        # Ensure only one user exists
        self.auth.cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", ("client_user",))
        count = self.auth.cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_login_failure(self):
        self.auth.register("someone", "somepassword", "client")
        role = self.auth.login("someone", "wrongpassword")
        self.assertIsNone(role)


if __name__ == "__main__":
    unittest.main()
