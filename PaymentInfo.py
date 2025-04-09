import datetime

class PaymentInfo:
    def __init__(self, unavailable_dates=None):
        """Initializes a payment record with user input and checks for unavailable dates."""
        if unavailable_dates is None:
            unavailable_dates = []

        while True:
            self.pay_date = input("Enter payment date (MM-DD): ")
            try:
                self.date_obj = datetime.datetime.strptime(self.pay_date, "%m-%d")  # Validate format
                if self.pay_date in unavailable_dates:
                    print("Error: Selected date is unavailable. Please choose another date.")
                else:
                    break
            except ValueError:
                print("Error: Invalid date format. Please enter a valid date (MM-DD).")

        self.pay_user = input("Enter name of user making the payment: ")
        self.service = self.choose_service()
        self.pay_total = self.set_payment(self.service)

    def choose_service(self):
        """Allows user to choose a service."""
        services = {"1": ("Haircut", 40), "2": ("Shave", 20)}
        while True:
            print("Choose a service:")
            print("1. Haircut ($40)")
            print("2. Shave ($20)")
            choice = input("Enter 1 or 2: ")
            if choice in services:
                return services[choice]
            print("Invalid choice. Please select a valid service.")

    def set_payment(self, service):
        """Sets the payment amount based on the service chosen."""
        return service[1]

    def display_payment(self):
        """Displays payment details."""
        formatted_date = self.date_obj.strftime("%B %d")  # Month name and day
        return (f"Payment Details:\nDate: {formatted_date}\nUser: {self.pay_user}\n"
                f"Service: {self.service[0]}\nTotal: ${self.pay_total:.2f}")

# Example usage:
unavailable_dates = ["03-20", "03-25"]  # Example unavailable dates
payment = PaymentInfo(unavailable_dates)
print(payment.display_payment())
