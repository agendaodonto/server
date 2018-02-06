from django.conf import settings

from app.schedule.celery import celery_app
from app.schedule.libs.sms import DeviceNotFoundError


@celery_app.task(bind=True)
def send_message(self, to, message):
    messenger = settings.APP_MESSENGER_CLASS
    user = settings.SMS_GATEWAY_USER
    password = settings.SMS_GATEWAY_PASSWORD
    try:
        messenger = messenger(user, password)
        messenger.get_best_device()
        return messenger.send_message(to, message)
    except DeviceNotFoundError as e:
        self.retry(exc=e, max_retries=settings.CELERY_TASK_MAX_RETRY, countdown=60 * 5)
