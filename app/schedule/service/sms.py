from datetime import datetime
from time import sleep

from django.conf import settings
from pyfcm import FCMNotification


class SMS:
    def __init__(self):
        self.client = FCMNotification(settings.FIREBASE_TOKEN)

    def wait_for_status_change(self, schedule) -> bool:
        start_time = datetime.now()
        timeout = settings.SMS_TIMEOUT
        previous_status = schedule.notification_status
        status_changed = False

        while not status_changed:
            if schedule.notification_status != previous_status:
                status_changed = True
            if (datetime.now() - start_time).total_seconds() >= timeout:
                raise SMSTimeoutError('Tempo excedido')
            sleep(1)

        return True

    def send_message(self, schedule):
        self.client.single_device_data_message(schedule.dentist.device_token, data_message={
            'sendTo': schedule.patient.phone,
            'content': schedule.get_message(),
            'scheduleId': schedule.id
        })

        return self.wait_for_status_change(schedule)


class FakeSMS:
    def send_message(self, schedule):
        return True


class SMSTimeoutError(BaseException):
    pass
