from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from .services import PaymentService


class PaymentServiceTests(TestCase):

    def test_calculate_payment_with_large_numbers(self):
        self.assertEqual(PaymentService.calculate_payment(1000000, Decimal('1000000')), Decimal('1000000000000'))

    def test_calculate_payment_with_zero_hours(self):
        self.assertEqual(PaymentService.calculate_payment(0, Decimal('100')), Decimal('0'))

    def test_calculate_payment_with_non_numeric_input(self):
        with self.assertRaises(ValueError):
            PaymentService.calculate_payment("five", Decimal('100'))
        with self.assertRaises(ValueError):
            PaymentService.calculate_payment(5, "hundred")

    def test_calculate_payment_with_negative_input(self):
        with self.assertRaises(ValueError):
            PaymentService.calculate_payment("five", -Decimal('100'))
