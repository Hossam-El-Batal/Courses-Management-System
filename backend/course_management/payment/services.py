
from decimal import Decimal


class PaymentService:
    @staticmethod
    def calculate_payment(hours_worked, hourly_rate):

        if not isinstance(hours_worked, (int, float, Decimal)) or not isinstance(hourly_rate, (int, float, Decimal)):
            raise ValueError("Both hours_worked and hourly_rate must be numeric values.")

        if hours_worked < 0 or hourly_rate < 0:
            raise ValueError("Hours worked and hourly rate must be non-negative")
        return hours_worked * hourly_rate
