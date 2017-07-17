import json

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from app.schedule.models import Dentist


class DentistAPITest(APITestCase):
    def setUp(self):
        self.dentist = Dentist.objects.create_user('John', 'Snow', 'john@snow.com', 'M', '1234', 'SP', 'john')
        self.extra_dentist = Dentist.objects.create_user('Maria', 'Dolores', 'maria@d.com', 'F', '5555', 'RJ', 'maria')
        self.api_authentication()

    def api_authentication(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(self.dentist)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def test_get_dentist(self):
        url = reverse('dentists') + '?cro=234'

        response = self.client.get(url)

        self.assertEqual(len(json.loads(response.content.decode('utf-8'))),
                         Dentist.objects.filter(cro__contains='234').count())
        self.assertEqual(200, response.status_code)
