#!/bin/bash

set -e

echo "${0}: making migrations"
python manage.py makemigrations

echo "${0}: running migrations"
python manage.py migrate --noinput

echo "${0}: running server"
exec python manage.py runserver 0.0.0.0:8000
