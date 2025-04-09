class AppointmentInfo:
    def __init__(self, app_date: str, app_time: str, app_employee: str, app_service: str, app_payment: str):
        self.app_date = app_date
        self.app_time = app_time
        self.app_client = app_client
        self.app_request = app_service
        self.app_service = app_payment

    def set_app(self, app_date: str, app_time: str):
        self.app_date = app_date
        self.app_time = app_time

    def display_date(self):
        return f"Appointment Date: {self.app_date}, Time: {self.app_time}"

    def get_appointment(self):
        return f"Appointment Summary: \nDate: {self.app_date} \nTime: {self.app_time} \nEmployee: {self.app_client} \nService: {self.app_service} \nPayment: {self.app_payment}"

# Example Usage
if __name__ == "__main__":
    appointment = AppointmentInfo("2025-05-20", "10:00 AM", "Kyle", "Tattoo, "$250")
    print(appointment.display_date())
    print(appointment.get_appointment())
