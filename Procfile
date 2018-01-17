web: gunicorn app.wsgi --log-file -
worker: celery -A app.schedule worker --concurrency 4 --without-gossip --without-mingle --without-heartbeat --loglevel=info
release: python manage.py migrate --no-input
