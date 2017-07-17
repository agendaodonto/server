import dj_database_url

from .default import *

DATABASES = {'default': dj_database_url.config()}

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

DJOSER['DOMAIN'] = 'agendaodontoweb-staging.firebaseapp.com'

CELERY_BROKER_URL = os.environ['CLOUDAMQP_URL']

MESSAGE_ETA = {'hour': 0, 'minute': 0}
MESSAGE_EXPIRES = {'hour': 23, 'minute': 59}
