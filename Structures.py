import datetime
from PaymentInfo import PaymentInfo


class FinancialRecords:
    def __init__(self):
        self.records = []  # List to store PaymentInfo objects
        self.unavailable_dates = ["03-20", "03-25"]  # Example unavailable dates

    def add_record(self, client_name, amount, date):
        try:
            payment = PaymentInfo(date, amount, client_name, self.unavailable_dates)
            self.records.append(payment)
        except ValueError as e:
            print(e)

    def get_records(self):
        return [record.display_payment() for record in self.records]

    def total_revenue(self):
        return sum(record.pay_total for record in self.records)


class Appointments:
    def __init__(self):
        self.appointments = []  # List to store appointment details

    def add_appointment(self, client_name, date, time):
        self.appointments.append({
            "client_name": client_name,
            "date": date,
            "time": time
        })

    def get_appointments(self):
        return self.appointments


class Client:
    def __init__(self, name: str, contact_info: str):
        self.name = name
        self.contact_info = contact_info
        self.financial_records = FinancialRecords()
        self.appointments = Appointments()

    def display_info(self):
        return f"Client Name: {self.name}\nContact Info: {self.contact_info}"


class Admin:
    def __init__(self, name: str, contact_info: str):
        self.name = name
        self.contact_info = contact_info
        self.financial_records = FinancialRecords()
        self.appointments = Appointments()

    def display_info(self):
        return f"Admin Name: {self.name}\nContact Info: {self.contact_info}"

    def add_client_payment(self, client, amount, date):
        client.financial_records.add_record(client.name, amount, date)
        self.financial_records.add_record(client.name, amount, date)

    def schedule_appointment(self, client, date, time):
        client.appointments.add_appointment(client.name, date, time)
        self.appointments.add_appointment(client.name, date, time)

    def view_client_info(self, client):
        return client.display_info()

    def view_client_records(self, client):
        return client.financial_records.get_records()

    def view_client_appointments(self, client):
        return client.appointments.get_appointments()

    def display_financial(self):
        return f"Total Revenue: ${self.financial_records.total_revenue()}"

    def gen_client_rep(self, client):
        return {
            "Client Info": client.display_info(),
            "Appointments": client.appointments.get_appointments()
        }

    def gen_fin_rep(self):
        return {
            "Total Revenue": self.financial_records.total_revenue(),
            "Financial Records": self.financial_records.get_records()
        }

    def gen_app_sch(self):
        return self.appointments.get_appointments()


# Example usage
admin1 = Admin("John Doe", "johndoe@example.com")
client1 = Client("Client A", "clienta@example.com")
client2 = Client("Client B", "clientb@example.com")
client3 = Client("Client C", "clientc@example.com")

admin1.add_client_payment(client1, 500, "03-19")
admin1.add_client_payment(client1, 200, "03-20")  # Should show an error due to unavailable date
admin1.add_client_payment(client2, 300, "03-21")
admin1.add_client_payment(client2, 150, "03-22")
admin1.add_client_payment(client3, 700, "03-23")
admin1.add_client_payment(client3, 400, "03-25")  # Should show an error due to unavailable date

admin1.schedule_appointment(client1, "03-21", "10:00 AM")
admin1.schedule_appointment(client1, "03-24", "11:00 AM")
admin1.schedule_appointment(client2, "03-22", "2:00 PM")
admin1.schedule_appointment(client2, "03-25", "3:00 PM")
admin1.schedule_appointment(client3, "03-23", "1:00 PM")
admin1.schedule_appointment(client3, "03-26", "4:00 PM")

print(admin1.display_info())
print("Financial Records:", admin1.financial_records.get_records())
print("Appointments:", admin1.appointments.get_appointments())
print("Total Revenue:", admin1.display_financial())
print("Client Report (Client A):", admin1.gen_client_rep(client1))
print("Client Report (Client B):", admin1.gen_client_rep(client2))
print("Client Report (Client C):", admin1.gen_client_rep(client3))
print("Financial Report:", admin1.gen_fin_rep())
print("Appointment Schedule:", admin1.gen_app_sch())

print(client1.display_info())
print("Client A Financial Records:", client1.financial_records.get_records())
print("Client A Appointments:", client1.appointments.get_appointments())

print(client2.display_info())
print("Client B Financial Records:", client2.financial_records.get_records())
print("Client B Appointments:", client2.appointments.get_appointments())

print(client3.display_info())
print("Client C Financial Records:", client3.financial_records.get_records())
print("Client C Appointments:", client3.appointments.get_appointments())
