# Generated by Django 4.2.17 on 2025-01-05 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_coursetrainerhours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
