#!/bin/sh

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py loaddata cities dev
uvicorn FantasyStore.asgi:application --host 0.0.0.0 --port 8000 --reload
