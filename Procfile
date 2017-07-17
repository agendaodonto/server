web: gunicorn scheduleserver.wsgi --log-file -
worker: celery -A scheduleserver.schedule worker --loglevel=info
