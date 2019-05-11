import json

from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from app.schedule.models import Dentist, Clinic, DentalPlan


class DentalPlanAPITest(APITestCase):
    def setUp(self):
        self.dentist = Dentist.objects.create_user('John', 'Snow', 'john@snow.com', 'M', '1234', 'SP', 'john')
        self.clinic = Clinic.objects.create(
            name='Test Clinic',
            owner=self.dentist,
            message='',
            time_delta=0
        )
        self.authenticate()

    def authenticate(self):
        token = Token.objects.create(user=self.dentist)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_dental_plan_list(self):
        url = reverse('dental-plans')
        DentalPlan.objects.create(name='some plan')
        response = self.client.get(url)

        self.assertEqual(len(json.loads(response.content.decode('utf-8'))), DentalPlan.objects.count())
        self.assertEqual(200, response.status_code)

    def test_get_dental_plan(self):
        plan = DentalPlan.objects.create(name='some plan')
        url = reverse('dental-plan-detail', kwargs={"pk": plan.pk})

        response = self.client.get(url)

        self.assertEqual(json.loads(response.content.decode('utf-8')).get('name'), DentalPlan.objects.first().name)
        self.assertEqual(200, response.status_code)

    def test_create_dental_plan(self):
        url = reverse('dental-plans')

        body = {
            'name': 'Test Plan'
        }

        response = self.client.post(url, body)

        self.assertEqual(Clinic.objects.count(), 1)
        self.assertEqual(response.status_code, 201)

    def test_edit_dental_plan(self):
        plan = DentalPlan.objects.create(name='some plan')

        url = reverse('dental-plan-detail', kwargs={"pk": plan.pk})

        body = {
            'name': 'Some Plan'
        }

        response = self.client.put(url, body)
        plan.refresh_from_db()
        self.assertEqual(200, response.status_code)
        self.assertEqual(plan.name, body['name'])
