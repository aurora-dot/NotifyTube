#!/bin/bash

### Django setup ###
python manage.py migrate --no-input
python manage.py createsuperuser --no-input

### Install npm dependencies and build tailwind ###
npm install && npm run build

### Collect static after generating tailwind output
python manage.py collectstatic --noinput
