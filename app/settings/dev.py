import datetime

from .default import *

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'app',
#         'USER': 'postgres',
#         'PASSWORD': 'test',
#         'HOST': '192.168.1.26',
#         'PORT': '5432',
#     }
# }

CORS_ORIGIN_ALLOW_ALL = True

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=10)
}

APP_MESSENGER_CLASS = 'app.schedule.libs.sms.DummySMS'
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATE = True
