from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from trainer.models import Trainer
from course.models import Course


class CourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.course_data = {
            'title': 'TypeScript Fundamentals',
            'description': 'practice typescript',
            'duration_hours': 20,
            'price': '199.99',
            'start_date': '2024-01-01',
            'end_date': '2024-01-31'
        }

    def test_course_operations(self):
        response = self.client.post(reverse('create-course'), self.course_data)
        self.assertEqual(response.status_code, 302)

        invalid_data = self.course_data.copy()
        invalid_data['end_date'] = '2023-12-31'
        response = self.client.post(reverse('create-course'), invalid_data)
        self.assertEqual(response.status_code, 200)

        trainer = Trainer.objects.create(
            name='test trainer',
            email='test@example.com',
            phone='123456789',
            expertise='Python',
            hourly_rate=Decimal('75.00')
        )
        course = Course.objects.first()
        response = self.client.post(
            reverse('assign-trainer', args=[course.pk]),
            {'trainer_id': trainer.id}
        )
        self.assertEqual(response.status_code, 302)

    def test_trainer_assignment(self):
        # Create course and assign non-existent trainer
        course = Course.objects.create(**self.course_data)
        response = self.client.post(
            reverse('assign-trainer', args=[course.pk]),
            {'trainer_id': 999}
        )
        self.assertEqual(response.status_code, 404)

    def test_some_edge_cases(self):

        # date input difference
        invalid_data = self.course_data.copy()
        invalid_data['end_date'] = '2023-12-31'
        response = self.client.post(reverse('create-course'), invalid_data)
        self.assertEqual(response.status_code, 200)

        # zero duration input
        invalid_data = self.course_data.copy()
        invalid_data['duration_hours'] = 0
        response = self.client.post(reverse('create-course'), invalid_data)
        self.assertEqual(response.status_code, 200)