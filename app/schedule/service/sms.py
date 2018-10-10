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
                print('FINALLYYY !! STATUS HAS BEEN CHANGED!')
            if (datetime.now() - start_time).total_seconds() >= timeout:
                schedule.notification_status = 3
                raise SMSTimeoutError('Tempo excedido')
            print('WAITING!!!')
            sleep(1)

        return True

    def send_message(self, schedule_id):
        from app.schedule.models import Schedule
        schedule = Schedule.objects.get(pk=schedule_id)
        self.client.single_device_data_message(schedule.dentist.device_token, data_message={
            'sendTo': schedule.patient.phone,
            'content': schedule.get_message(),
            'scheduleId': schedule.id
        })
        print('AHHHH WORKING!!!')
        return self.wait_for_status_change(schedule)


class FakeSMS:
    def send_message(self, schedule):
        return True


class SMSTimeoutError(BaseException):
    pass
