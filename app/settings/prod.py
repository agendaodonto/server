import dj_database_url
from .default import *

DEBUG = False

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', None)

ALLOWED_HOSTS = ['agendaodonto.herokuapp.com']

DATABASES = {'default': dj_database_url.config()}

CORS_ORIGIN_WHITELIST = ('agendaodonto.herokuapp.com', 'https://agendaodonto-29023.firebaseapp.com', 'http://agendaodonto-29023.firebaseapp.com', 'agendaodonto-29023.firebaseapp.com')

DJOSER['DOMAIN'] = 'agendaodonto-29023.firebaseapp.com'
