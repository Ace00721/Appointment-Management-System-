import datetime


class PaymentInfo:
    def __init__(self, unavailable_dates=None):
        """Initializes a payment record with user input and checks for unavailable dates."""
        if unavailable_dates is None:
            unavailable_dates = []

        while True:
            self.pay_date = input("Enter payment date (MM-DD): ")
            try:
                date_obj = datetime.datetime.strptime(self.pay_date, "%m-%d").date()
                if self.pay_date in unavailable_dates:
                    print("Error: Selected date is unavailable. Please choose another date.")
                else:
                    break
            except ValueError:
                print("Error: Invalid date format. Please enter a valid date (MM-DD).")

        self.pay_total = float(input("Enter payment amount: "))
        self.pay_user = input("Enter name of user making the payment: ")

    def set_payment(self, payment: float):
        """Sets the payment amount."""
        self.pay_total = payment

    def display_payment(self):
        """Displays payment details."""
        return f"Payment Details:\nDate: {self.pay_date}\nTotal: ${self.pay_total:.2f}\nUser: {self.pay_user}"


"Sets dates for unavailable dates "
unavailable_dates = ["03-20","03-25"]
payment = PaymentInfo(unavailable_dates)
print(payment.display_payment())
