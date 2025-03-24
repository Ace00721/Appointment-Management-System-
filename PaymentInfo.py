import datetime


class PaymentInfo:
    def __init__(self, pay_date, pay_user, service_choice=None, service_name=None, service_price=None, unavailable_dates=None):
        """Initializes a payment record with given parameters and checks for unavailable dates."""
        if unavailable_dates is None:
            unavailable_dates = []

        try:
            datetime.datetime.strptime(pay_date, "%m-%d")  # Validate format
            if pay_date in unavailable_dates:
                raise ValueError("Error: Selected date is unavailable. Please choose another date.")
        except ValueError as e:
            raise ValueError(f"Error: Invalid date format or unavailable date. {e}")

        self.pay_date = pay_date
        self.pay_user = pay_user
        self.service = self.choose_service(service_choice, service_name, service_price)
        self.pay_total = self.set_payment(self.service)

    def choose_service(self, service_choice, service_name, service_price):
        """Selects a service based on choice or direct input."""
        services = {"1": ("Haircut", 40), "2": ("Shave", 20)}
        if service_choice in services:
            return services[service_choice]
        elif service_name and service_price:
            return (service_name, service_price)
        raise ValueError("Invalid service selection. Provide a valid choice or specify a service name and price.")

    def set_payment(self, service):
        """Sets the payment amount based on the service chosen."""
        return service[1]

    def display_payment(self):
        """Displays payment details."""
        return (f"Payment Details:\nDate: {self.pay_date}\nUser: {self.pay_user}\n"
                f"Service: {self.service[0]}\nTotal: ${self.pay_total:.2f}")


# Example usage:
unavailable_dates = ["03-20", "03-25"]  # Example unavailable dates
try:
    payment1 = PaymentInfo("03-21", "John Doe", service_choice="1", unavailable_dates=unavailable_dates)
    print(payment1.display_payment())
    
    payment2 = PaymentInfo("03-22", "Jane Doe", service_name="Custom Service", service_price=50, unavailable_dates=unavailable_dates)
    print(payment2.display_payment())
except ValueError as e:
    print(e)
