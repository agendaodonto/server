from django.conf import settings

from app.schedule.celery import celery_app


@celery_app.task(bind=True)
def send_message(self, to, message):
    # messenger = settings.APP_MESSENGER_CLASS
    # token = settings.SMS_GATEWAY_TOKEN
    # try:
        # messenger = messenger(token)
        # messenger.get_latest_device()
        # return messenger.send_message(to, message)
    # except DeviceNotFoundError as e:
    #     self.retry(exc=e, max_retries=settings.CELERY_TASK_MAX_RETRY, countdown=60 * 5)
    pass
