from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Trainer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True,null=False)
    phone = models.CharField(max_length=20)
    expertise = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
