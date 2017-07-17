import json
import time
from datetime import datetime, timedelta

import pytz
from django.core.urlresolvers import reverse
from django.test import TestCase
from requests_mock import Mocker
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from app.schedule.libs.sms import SMS
from app.schedule.libs.sms_gateway import SMSGateway
from app.schedule.models import Schedule
from app.schedule.models.clinic import Clinic
from app.schedule.models.dentist import Dentist
from app.schedule.models.patient import Patient


class ScheduleAPITest(APITestCase):
    def setUp(self):
        self.dentist = Dentist.objects.create_user('John', 'Snow', 'john@snow.com', 'M', '1234', 'SP', 'john')
        self.extra_dentist = Dentist.objects.create_user('Maria', 'Dolores', 'maria@d.com', 'F', '5555', 'RJ', 'maria')
        self.clinic = Clinic.objects.create(
            name='Test Clinic',
            owner=self.dentist,
            message='',
            time_delta=1.0
        )
        self.clinic.dentists.add(self.dentist)
        self.clinic.dentists.add(self.extra_dentist)
        self.patient = Patient.objects.create(
            name='Luís',
            last_name='Cunha Martins',
            phone='+5519993770437',
            sex='M',
            clinic=self.clinic
        )
        self.schedule = Schedule.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date=datetime.now(tz=pytz.timezone('America/Sao_Paulo')),
            duration=60
        )

        self.api_authentication()

    def api_authentication(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(self.dentist)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def test_get_schedule(self):
        url = reverse('schedules')
        Schedule.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date=datetime.now(tz=pytz.timezone('America/Sao_Paulo')),
            duration=60
        )
        response = self.client.get(url)
        self.assertEqual(len(json.loads(response.content.decode('utf-8'))), Schedule.objects.count())
        self.assertEqual(200, response.status_code)

    def test_filter_schedule(self):
        url = reverse('schedules') + '?date_0=10/5/2016&date_1=11/5/2016'
        Schedule.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date=datetime(2016, 5, 10, tzinfo=pytz.UTC),
            duration=60
        )

        Schedule.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date=datetime(2016, 5, 11, tzinfo=pytz.UTC),
            duration=60
        )

        Schedule.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date=datetime(2016, 5, 12, tzinfo=pytz.UTC),
            duration=60
        )

        response = self.client.get(url)
        response_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response_data))

    def test_create_schedule(self):
        url = reverse('schedules')
        body = {
            'patient': self.patient.id,
            'dentist': self.dentist.id,
            'date': datetime.now(tz=pytz.timezone('America/Sao_Paulo')),
            'duration': 60
        }

        response = self.client.post(url, body)

        self.assertEqual(201, response.status_code)
        self.assertEqual(2, Schedule.objects.count())

    def test_edit_schedule(self):
        url = reverse('schedule-detail', kwargs={"pk": self.schedule.pk})

        body = {
            'patient': self.patient.id,
            'dentist': self.dentist.id,
            'date': datetime.now(tz=pytz.timezone('America/Sao_Paulo')),
            'duration': 50
        }

        response = self.client.put(url, body)

        response_data = json.loads(response.content.decode('utf-8'))

        schedule = Schedule.objects.get(id=self.schedule.id)

        self.assertEqual(response_data.get('duration'), schedule.duration)

    def test_delete_schedule(self):
        url = reverse('schedule-detail', kwargs={"pk": self.schedule.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

    def test_get_attendance(self):
        url = reverse('schedule-attendance')

        y = datetime.now().year

        Schedule.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date=datetime(y, 5, 11, tzinfo=pytz.UTC),
            duration=60,
            status=1
        )

        Schedule.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date=datetime(y, 5, 11, tzinfo=pytz.UTC),
            duration=60,
            status=2
        )

        Schedule.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date=datetime(y, 5, 11, tzinfo=pytz.UTC),
            duration=60,
            status=3
        )

        Schedule.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date=datetime(y + 1, 5, 11, tzinfo=pytz.UTC),
            duration=60,
            status=3
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response_data['attendances'][4], 1)
        self.assertEqual(response_data['absences'][4], 1)
        self.assertEqual(response_data['cancellations'][4], 1)


class ScheduleNotificationTest(TestCase):
    DEVICES_MOCK = "{\"success\": \"True\", \"result\": {\"data\": [{\"model\": \"SM-G930F\", \"battery\": \"50\", \"wifi\": \"1\", \"provider\": \"TIMBRASIL | TIM\", \"id\": \"123456\", \"created_at\": \"False\", \"last_seen\": " + str(
        int(
            time.time())) + ", \"country\": \"br\", \"lng\": \"-47.1592126\", \"signal\": \"100\", \"number\": \"\", \"make\": \"Samsung\", \"lat\": \"-22.8414491\", \"name\": \"Device 28982\", \"connection_type\": \"4G\"}, {\"model\": \"SM-G930F\", \"battery\": \"100\", \"wifi\": \"0\", \"provider\": \"CLARO BR\", \"id\": \"29772\", \"created_at\": \"False\", \"last_seen\": " + str(
        int(
            time.time())) + ", \"country\": \"br\", \"lng\": \"0\", \"signal\": \"60\", \"number\": \"\", \"make\": \"Samsung\", \"lat\": \"0\", \"name\": \"Device 29772\", \"connection_type\": \"4G\"}], \"per_page\": 500, \"current_page\": 1, \"from\": 1, \"total\": 2, \"to\": 2, \"last_page\": 1}}"
    DEVICES_NOT_AVAILABLE_MOCK = "{\"success\": \"True\", \"result\": {\"data\": [{\"model\": \"SM-G930F\", \"battery\": \"13\", \"wifi\": \"1\", \"provider\": \"TIMBRASIL | TIM\", \"id\": \"123456\", \"created_at\": \"False\", \"last_seen\": " + str(
        int(
            time.time())) + ", \"country\": \"br\", \"lng\": \"-47.1592126\", \"signal\": \"80\", \"number\": \"\", \"make\": \"Samsung\", \"lat\": \"-22.8414491\", \"name\": \"Device 28982\", \"connection_type\": \"4G\"},{\"model\": \"SM-G935F\", \"battery\": \"13\", \"wifi\": \"1\", \"provider\": \"TIMBRASIL | TIM\", \"id\": \"55555\", \"created_at\": \"False\", \"last_seen\":" + str(
        int(
            time.time())) + ", \"country\": \"br\", \"lng\": \"-47.1592126\", \"signal\": \"0\", \"number\": \"\", \"make\": \"Samsung\", \"lat\": \"-22.8414491\", \"name\": \"Device 28982\", \"connection_type\": \"4G\"},{\"model\": \"SM-G930F\", \"battery\": \"100\", \"wifi\": \"0\", \"provider\": \"CLARO BR\", \"id\": \"29772\", \"created_at\": \"False\", \"last_seen\": 1474735362, \"country\": \"br\", \"lng\": \"0\", \"signal\": \"80\", \"number\": \"\", \"make\": \"Samsung\", \"lat\": \"0\", \"name\": \"Device 29772\", \"connection_type\": \"4G\"}], \"per_page\": 500, \"current_page\": 1, \"from\": 1, \"total\": 2, \"to\": 2, \"last_page\": 1}}"
    MESSAGE_MOCK = "{\"result\": {\"fails\": [], \"success\": [{\"error\": \"\", \"queued_at\": 0, \"device_id\": \"28982\", \"status\": \"pending\", \"delivered_at\": 0, \"sent_at\": 0, \"created_at\": 1474737310, \"expires_at\": 1474740910, \"canceled_at\": 0, \"contact\": {\"id\": \"3655322\", \"number\": \"+5519993770437\", \"name\": \"+5519993770437\"}, \"id\": \"24081213\", \"message\": \"blah\", \"send_at\": 1474737310, \"received_at\": 0, \"failed_at\": 0}]}, \"success\": \"True\"}"
    MESSAGE_SENT_MOCK = "{\"result\": {\"canceled_at\": 0, \"received_at\": 0, \"send_at\": 1474936985, \"delivered_at\": 0, \"expires_at\": 1474940585, \"error\": \"\", \"status\": \"sent\", \"queued_at\": 1474980195, \"contact\": {\"id\": \"4308251\", \"name\": \"Andr&eacute; Roggeri Campos\", \"number\": \"993770437\"}, \"id\": \"24246261\", \"created_at\": 1474936985, \"sent_at\": 0, \"failed_at\": 0, \"message\": \"teste\", \"device_id\": \"28982\"}, \"success\": \"True\"}"
    MESSAGE_FAILED_MOCK = "{\"result\": {\"canceled_at\": 0, \"received_at\": 0, \"send_at\": 1474936985, \"delivered_at\": 0, \"expires_at\": 1474940585, \"error\": \"\", \"status\": \"failed\", \"queued_at\": 1474980195, \"contact\": {\"id\": \"4308251\", \"name\": \"Andr&eacute; Roggeri Campos\", \"number\": \"993770437\"}, \"id\": \"24246261\", \"created_at\": 1474936985, \"sent_at\": 0, \"failed_at\": 0, \"message\": \"teste\", \"device_id\": \"28982\"}, \"success\": \"True\"}"
    MESSAGE_STUCK_MOCK = "{\"result\": {\"canceled_at\": 0, \"received_at\": 0, \"send_at\": 1474936985, \"delivered_at\": 0, \"expires_at\": 1474940585, \"error\": \"\", \"status\": \"queued\", \"queued_at\": 1474980195, \"contact\": {\"id\": \"4308251\", \"name\": \"Andr&eacute; Roggeri Campos\", \"number\": \"993770437\"}, \"id\": \"24246261\", \"created_at\": 1474936985, \"sent_at\": 0, \"failed_at\": 0, \"message\": \"teste\", \"device_id\": \"28982\"}, \"success\": \"True\"}"

    def setUp(self):
        self.dentist = Dentist.objects.create_user('John', 'Snow', 'john@snow.com', 'M', '1234', 'SP', 'john')
        self.clinic = Clinic.objects.create(
            name='Test Clinic',
            owner=self.dentist,
            message='',
            time_delta=1.0
        )
        self.patient = Patient.objects.create(
            name='Luís',
            last_name='Cunha Martins',
            phone='+5519993770437',
            sex='M',
            clinic=self.clinic
        )
        self.schedule = Schedule.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date=datetime(2016, 9, 15, 15, 0, tzinfo=pytz.utc),
            duration=60
        )

    def test_get_schedule_message_any_date(self):
        expected = "Olá Sr. Luís, " \
                   "não se esqueça de sua consulta odontológica " \
                   "dia 15/09 às 12:00."

        self.assertEqual(self.schedule.get_message(), expected)

    def test_get_schedule_message_today(self):
        self.schedule.date = datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
        expected = "Olá Sr. Luís, " \
                   "não se esqueça de sua consulta odontológica " \
                   "hoje às {}.".format(self.schedule.date.strftime("%H:%M"))

        self.assertEqual(self.schedule.get_message(), expected)

    def test_get_schedule_message_tomorrow(self):
        self.schedule.date = datetime.now(tz=pytz.timezone('America/Sao_Paulo')) + timedelta(days=1)
        expected = "Olá Sr. Luís, " \
                   "não se esqueça de sua consulta odontológica " \
                   "amanhã às {}.".format(self.schedule.date.strftime("%H:%M"))

        self.assertEqual(self.schedule.get_message(), expected)

    def test_get_best_device(self):
        with Mocker() as m:
            m.get(SMSGateway.BASE_URL + '/api/v3/devices', text=self.DEVICES_MOCK)
            sms = SMS('test', 'bbb')

            self.assertEqual('123456', sms.get_best_device())

    def test_send_sms(self):
        with Mocker() as m:
            m.get(SMSGateway.BASE_URL + '/api/v3/devices', text=self.DEVICES_MOCK)
            m.post(SMSGateway.BASE_URL + '/api/v3/messages/send', text=self.MESSAGE_MOCK)
            m.get(SMSGateway.BASE_URL + '/api/v3/messages/view/24081213', text=self.MESSAGE_SENT_MOCK)
            sms = SMS('test', 'bbb')

            self.assertTrue(sms.send_message('123456', 'test message'))

    def test_failed_sms(self):
        with Mocker() as m:
            m.get(SMSGateway.BASE_URL + '/api/v3/devices', text=self.DEVICES_MOCK)
            m.post(SMSGateway.BASE_URL + '/api/v3/messages/send', text=self.MESSAGE_MOCK)
            m.get(SMSGateway.BASE_URL + '/api/v3/messages/view/24081213', text=self.MESSAGE_FAILED_MOCK)
            sms = SMS('test', 'bbb')

            self.assertFalse(sms.send_message('123456', 'test message'))

    def test_stuck_sms(self):
        with Mocker() as m:
            m.get(SMSGateway.BASE_URL + '/api/v3/devices', text=self.DEVICES_MOCK)
            m.post(SMSGateway.BASE_URL + '/api/v3/messages/send', text=self.MESSAGE_MOCK)
            m.get(SMSGateway.BASE_URL + '/api/v3/messages/view/24081213', text=self.MESSAGE_STUCK_MOCK)
            sms = SMS('test', 'bbb')
            sms.SMS_TIMEOUT = 0.1

            self.assertFalse(sms.send_message('123456', 'test message'))

    def test_no_device_available(self):
        with Mocker() as m:
            m.get(SMSGateway.BASE_URL + '/api/v3/devices', text=self.DEVICES_NOT_AVAILABLE_MOCK)
