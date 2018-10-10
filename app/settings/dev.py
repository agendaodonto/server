import datetime

from .default import *

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

CORS_ORIGIN_ALLOW_ALL = True

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=10)
}

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATE = True

MESSAGE_ETA = {'hour': 0, 'minute': 0}
MESSAGE_EXPIRES = {'hour': 23, 'minute': 59}
