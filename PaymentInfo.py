import datetime

class PaymentInfo:
    def __init__(self, pay_date: str, pay_total: float, pay_user: str, unavailable_dates=None):
        """Initializes a payment record and checks for unavailable dates."""
        if unavailable_dates is None:
            unavailable_dates = []

        try:
            datetime.datetime.strptime(pay_date, "%m-%d")  # Validate date format
            if pay_date in unavailable_dates:
                raise ValueError(f"Error: {pay_date} is unavailable for payments. Choose another date.")
        except ValueError as e:
            raise ValueError(f"Invalid date or format: {e}")

        self.pay_date = pay_date
        self.pay_total = pay_total
        self.pay_user = pay_user

    def display_payment(self):
        """Displays payment details."""
        return f"Payment Details:\nDate: {self.pay_date}\nTotal: ${self.pay_total:.2f}\nUser: {self.pay_user}"
