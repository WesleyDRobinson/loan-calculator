#!/bin/bash

set -e

echo "${0}: running migrationg"
python manage.py makemigrations --merge
python manage.py migrate --noinput
