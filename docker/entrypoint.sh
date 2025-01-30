#!/bin/bash

set -e

echo "${0}: running migrationg"
python manage.py makemigrations --merge
python manage.py migrate --noinput

echo "${0}: running server"
exec python manage.py runserver 0.0.0.0:8000
