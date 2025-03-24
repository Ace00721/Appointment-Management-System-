import datetime
from paymentinfo2 import PaymentInfo


class FinancialRecords:
    def __init__(self):
        self.records = []  # List to store PaymentInfo objects
        self.unavailable_dates = ["03-20", "03-25"]  # Example unavailable dates

    def add_record(self, client_name, amount, date, service_name=None, service_choice=None):
        try:
            payment = PaymentInfo(
                pay_date=date,
                pay_user=client_name,
                service_choice=service_choice,
                service_name=service_name,
                service_price=amount,
                unavailable_dates=self.unavailable_dates
            )
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

    def add_client_payment(self, client, amount, date, service_name=None, service_choice=None):
        client.financial_records.add_record(client.name, amount, date, service_name, service_choice)
        self.financial_records.add_record(client.name, amount, date, service_name, service_choice)

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
