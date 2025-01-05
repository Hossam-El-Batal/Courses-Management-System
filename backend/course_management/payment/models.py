from django.db import models
from trainer.models import Trainer
from course.models import Course
from .services import PaymentService
from decimal import Decimal


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled')
    ]

    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    hours_worked = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_payment(self):
        return PaymentService.calculate_payment(self.hours_worked, self.trainer.hourly_rate)

    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.calculate_payment()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for {self.trainer.name} - {self.course.title}"


class CourseTrainerHours(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='course_hours')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='trainer_hours')
    hours_worked = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['trainer', 'course']

    def __str__(self):
        return f"{self.trainer.name} - {self.course.title} ({self.hours_worked} hours)"
