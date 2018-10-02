from django.conf import settings

from app.schedule.celery import celery_app


@celery_app.task(bind=True)
def send_message(self, schedule_id):
    try:
        from app.schedule.models import Schedule
        messenger = settings.MESSAGE_CLASS()
        schedule = Schedule.objects.get(pk=schedule_id)
        return messenger.send_message(schedule)
    except TimeoutError as e:
        self.retry(exc=e, max_retries=settings.CELERY_TASK_MAX_RETRY, countdown=60 * 5)
