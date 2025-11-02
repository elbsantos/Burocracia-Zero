#!/bin/sh
set -e

if [ -f .env ]; then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

: "${DJANGO_WSGI_MODULE:?Need to set DJANGO_WSGI_MODULE env var (e.g. core.wsgi)}"
GUNICORN_CMD="gunicorn ${DJANGO_WSGI_MODULE}:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3} --log-level ${GUNICORN_LOG_LEVEL:-info}"
echo "Starting gunicorn: $GUNICORN_CMD"
exec $GUNICORN_CMD
