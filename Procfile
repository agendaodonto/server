release: python manage.py migrate --no-input
web: gunicorn app.wsgi --log-file -
worker: celery -A app.schedule worker --loglevel=info
