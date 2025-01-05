

class PaymentService:
    @staticmethod
    def calculate_payment(hours_worked, hourly_rate):
        if hours_worked < 0 or hourly_rate < 0:
            raise ValueError("Hours worked and hourly rate must be non-negative")
        return hours_worked * hourly_rate
