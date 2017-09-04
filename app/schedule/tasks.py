from importlib import import_module

from django.conf import settings

from app.schedule.celery import celery_app
from app.schedule.libs.sms import DeviceNotFoundError


@celery_app.task(bind=True)
def send_message(self, to, message, sg_user, sg_password):
    def load_sms_class():
        module_name, class_name = settings.APP_MESSENGER_CLASS.rsplit(".", 1)
        return getattr(import_module(module_name), class_name)

    sms_class = load_sms_class()
    try:
        messenger = sms_class(sg_user, sg_password)
        messenger.get_best_device()
        messenger.send_message(to, message)
    except DeviceNotFoundError as e:
        self.retry(exc=e, max_retries=settings.CELERY_TASK_MAX_RETRY, countdown=60 * 5)
