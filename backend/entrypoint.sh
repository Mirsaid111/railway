#!/bin/bash
echo 'Waiting for PostgreSQL...'
while ! python -c 'import socket; import os; sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); result = sock.connect_ex(("db", 5432)); sock.close(); exit(result)'; do 
  sleep 1
done

echo 'PostgreSQL is ready!'
cd src
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL || true
python manage.py runserver 0.0.0.0:8000