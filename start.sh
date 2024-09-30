#!/usr/bin/env bash

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

#gunicorn webrosters.wsgi:application  Iniciar Gunicorn (o el servidor que estés utilizando)
gunicorn webrosters.wsgi:application #--bind 0.0.0.0:8000
