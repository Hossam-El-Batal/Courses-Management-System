# Generated by Django 4.2.17 on 2025-01-05 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
        ('trainer', '0001_initial'),
        ('payment', '0003_payment_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseTrainerHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_worked', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainer_hours', to='course.course')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_hours', to='trainer.trainer')),
            ],
            options={
                'unique_together': {('trainer', 'course')},
            },
        ),
    ]
