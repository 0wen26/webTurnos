#!/usr/bin/env bash

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate



#echo "from turnos.models import Turno; Turno.objects.all().delete()" | python manage.py shell

#echo "from django.contrib.auth.models import User; User.objects.filter(username='admin', is_superuser=True).delete()" | python manage.py shell
#echo "Superusuario eliminado"

# Crear un superusuario si no existe
echo "from django.contrib.auth.models import User; User.objects.create_superuser('owencin', 'admin@example.com', 'Burgos09')" | python manage.py shell
echo "Superusuario creado"

#gunicorn webrosters.wsgi:application  Iniciar Gunicorn (o el servidor que estés utilizando)
gunicorn webrosters.wsgi:application #--bind 0.0.0.0:8000
