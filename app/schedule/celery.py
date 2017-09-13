from celery import Celery
from django.conf import settings

celery_app = Celery('messenger')

celery_app.conf.update(
    # timezone=settings.TIME_ZONE,
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,
    task_always_eager=settings.CELERY_ALWAYS_EAGER,
    task_eager_propagates=settings.CELERY_EAGER_PROPAGATE,
    broker_heartbeat=settings.CELERY_BROKER_HEARTBEAT,
    worker_send_task_events=settings.CELERY_SEND_EVENTS,
    event_queue_expires=settings.CELERY_EVENT_QUEUE_EXPIRES
)

celery_app.autodiscover_tasks()
