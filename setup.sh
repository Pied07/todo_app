#!/bin/bash

# install dependencies
pip install setuptools
pip install -r requirements.txt

# Run django command/s
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput