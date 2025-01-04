from django.db import models
from trainer.models import Trainer


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_hours = models.IntegerField()
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, related_name='courses')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
