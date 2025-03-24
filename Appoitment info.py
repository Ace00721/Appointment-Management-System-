class AppointmentInfo:
    def __init__(self, app_date: str, app_time: str, app_employee: str, app_request: str, app_service: str):
        self.app_date = app_date
        self.app_time = app_time
        self.app_employee = app_employee
        self.app_request = app_request
        self.app_service = app_service

    def set_app(self, app_date: str, app_time: str):
        self.app_date = app_date
        self.app_time = app_time

    def display_date(self):
        return f"Appointment Date: {self.app_date}, Time: {self.app_time}"

    def show_summ(self):
        return f"Appointment Summary: \nDate: {self.app_date} \nTime: {self.app_time} \nEmployee: {self.app_employee} \n Request: {self.app_request} \nService: {self.app_service}"

# Example Usage
if __name__ == "__main__":
    appointment = AppointmentInfo("2025-05-20", "10:00 AM", "Kyle", "Tattoo", "Standard")
    print(appointment.display_date())
    print(appointment.show_summ())
