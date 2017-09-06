import json
from datetime import datetime, timedelta

import pytz
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from requests_mock import Mocker
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from app.schedule.libs.sms import SMS, DeviceNotFoundError
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
        self.sms = SMS('aaa', 'bbb')

    def get_response(self, file_name, **kwargs) -> bin:
        with open('app/schedule/tests/sms_gateway_responses/{}.json'.format(file_name)) as file:
            return file.read()

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

    @override_settings(SMS_MIN_MISSING_TIME=99999999)
    def test_get_best_device(self):
        with Mocker() as m:
            m.get(SMSGateway.BASE_URL + '/api/v3/devices', text=self.get_response('devices'))

            self.assertEqual('1', self.sms.get_best_device())

    def test_send_sms(self):
        with Mocker() as m:
            m.post(SMSGateway.BASE_URL + '/api/v3/messages/send', text=self.get_response('message_sent'))
            m.get(SMSGateway.BASE_URL + '/api/v3/messages/view/1', text=self.get_response('message_received'))

            self.assertTrue(self.sms.send_message('123456', 'test message'))

    def test_failed_sms(self):
        with Mocker() as m:
            m.post(SMSGateway.BASE_URL + '/api/v3/messages/send', text=self.get_response('message_sent'))
            m.get(SMSGateway.BASE_URL + '/api/v3/messages/view/1', text=self.get_response('message_failed'))

            self.assertFalse(self.sms.send_message('123456', 'test message'))

    @override_settings(SMS_TIMEOUT=0.1)
    def test_failed_wait_sms(self):
        with Mocker() as m:
            m.get(SMSGateway.BASE_URL + '/api/v3/messages/view/1', text='<html', status_code=500)
            self.assertFalse(self.sms.wait_message_sent('1'))

    @override_settings(SMS_TIMEOUT=0.1)
    def test_stuck_sms(self):
        with Mocker() as m:
            m.post(SMSGateway.BASE_URL + '/api/v3/messages/send', text=self.get_response('message_sent'))
            m.get(SMSGateway.BASE_URL + '/api/v3/messages/view/1', text=self.get_response('message_pending'))

            self.assertFalse(self.sms.send_message('123456', 'test message'))

    def test_no_device_available(self):
        with Mocker() as m:
            m.get(SMSGateway.BASE_URL + '/api/v3/devices', text=self.get_response('devices_not_suitable'))
            self.assertRaises(DeviceNotFoundError, self.sms.get_best_device)

    def test_gateway_down(self):
        with Mocker() as m:
            m.get(SMSGateway.BASE_URL + '/api/v3/devices', text='<html', status_code=500)
            self.assertRaises(DeviceNotFoundError, self.sms.get_best_device)

    @override_settings(APP_MESSENGER_CLASS=SMS)
    def test_notification_task(self):
        with Mocker() as m:
            m.get(SMSGateway.BASE_URL + '/api/v3/devices', text=self.get_response('devices_not_suitable'))
            self.schedule.duration = 20
            self.assertRaises(DeviceNotFoundError, self.schedule.save)
