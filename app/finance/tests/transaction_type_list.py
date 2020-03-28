from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from app.finance.models import TransactionType
from app.finance.serializers.transaction_type import TransactionTypeSerializer
from app.finance.tests.utils.data import create_type
from app.schedule.models import Dentist, Clinic


class TransactionTypeListAPITest(APITestCase):
    def setUp(self):
        self.dentist = Dentist.objects.create_user('John', 'Snow', 'john@snow.com', 'M', '1234', 'SP', 'john')
        self.clinic = Clinic.objects.create(
            name='Test Clinic',
            owner=self.dentist,
            message='',
            time_delta=0
        )
        self.authenticate()
        self.serializer = TransactionTypeSerializer()

    def authenticate(self):
        token = Token.objects.create(user=self.dentist)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_should_get_transaction_types(self):
        # Arrange
        url = reverse('transaction-types')
        avail_transaction = create_type(self.clinic)

        # Act
        req = self.client.get(url)

        # Assert
        content = req.json()
        self.assertEqual(req.status_code, 200)
        self.assertEquals(content, [self.serializer.to_representation(avail_transaction)])

    def test_should_create_transaction_type(self):
        # Arrange
        url = reverse('transaction-types')

        # Act
        content = {
            'code': 1234,
            'clinic': self.clinic.id,
            'label': 'Some !!! Label1234'
        }
        req = self.client.post(url, content)

        # Assert
        transaction_types = TransactionType.objects.all()
        self.assertEqual(req.status_code, 201)
        self.assertEqual(transaction_types.count(), 1)
        self.assertEqual(self.serializer.to_representation(transaction_types[0]), content)

    def test_should_ensure_code_is_unique(self):
        # Arrange
        url = reverse('transaction-types')

        # Act
        content = {
            'code': 1234,
            'clinic': self.clinic.id,
            'label': 'Some !!! Label1234'
        }
        first_req = self.client.post(url, content)
        second_req = self.client.post(url, content.copy().update(label='some other'))

        # Assert
        transaction_types = TransactionType.objects.all()
        self.assertEqual(first_req.status_code, 201)
        self.assertEqual(second_req.status_code, 400)
        self.assertEqual(transaction_types.count(), 1)
        self.assertEqual(self.serializer.to_representation(transaction_types[0]), content)

    def test_should_only_return_transactions_type_for_clinics_owned_by_user(self):
        # Arrange
        other_dentist = Dentist.objects.create_user('John', 'Snow', 'aria@stark.com', 'F', '5599', 'SP', 'john')
        clinic2 = Clinic.objects.create(
            name='Test Clinic2',
            owner=self.dentist,
            message='',
            time_delta=0
        )
        clinic2.owner = other_dentist
        clinic2.save()

        url = reverse('transaction-types')
        avail_transaction1 = create_type(self.clinic)
        avail_transaction2 = create_type(clinic2)

        # Act
        req = self.client.get(url)

        # Assert
        content = req.json()
        self.assertEqual(req.status_code, 200)
        self.assertEquals(content, [self.serializer.to_representation(avail_transaction1)])
        self.assertNotContains(req, avail_transaction2.label)
