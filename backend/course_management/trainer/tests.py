from django.test import TestCase, Client
from django.urls import reverse


class TrainerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.trainer_data = {
            'name': 'test trainer',
            'email': 'test@example.com',
            'phone': '123456789',
            'expertise': 'Python',
            'hourly_rate': '75.00'
        }

    def test_trainer_crud_operations(self):
        # Create
        response = self.client.post(reverse('create-trainer'), self.trainer_data)
        self.assertEqual(response.status_code, 302)

        # Invalid phone entry
        invalid_data = self.trainer_data.copy()
        invalid_data['phone'] = 'abc123'
        response = self.client.post(reverse('create-trainer'), invalid_data)
        self.assertEqual(response.status_code, 200)

        # List
        response = self.client.get(reverse('list-trainers'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['trainers']), 1)

    def test_trainer_edge_cases(self):

        # Negative hourly rate
        invalid_data = self.trainer_data.copy()
        invalid_data['hourly_rate'] = '-50.00'
        response = self.client.post(reverse('create-trainer'), invalid_data)
        self.assertEqual(response.status_code, 200)

