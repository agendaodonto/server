release: python manage.py migrate --no-input
web: gunicorn app.wsgi --log-file - & celery -A app.schedule worker --loglevel=info
