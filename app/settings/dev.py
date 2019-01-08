import datetime

import dj_database_url

from .default import *

ALLOWED_HOSTS = ['*']

DATABASES = {'default': dj_database_url.config()}

CORS_ORIGIN_ALLOW_ALL = True

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=10)
}

# Celery Settings
CELERY_BROKER_URL = os.environ['RABBITMQ_URL']
CELERY_BROKER_HEARTBEAT = None

MESSAGE_ETA = {'hour': 0, 'minute': 0}
MESSAGE_EXPIRES = {'hour': 23, 'minute': 59}
