#!/usr/bin/env bash

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate



#echo "from turnos.models import Turno; Turno.objects.all().delete()" | python manage.py shell

echo "from django.contrib.auth.models import User; User.objects.filter(username='admin', is_superuser=True).delete()" | python manage.py shell
echo "Superusuario eliminado"

# Crear un superusuario si no existe
if [ -z "$(echo "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())" | python manage.py shell | tail -n 1)" ]; then
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'Burgos09')" | python manage.py shell
    echo "Superusuario creado"
else
    echo "El superusuario ya existe, no se ha creado ninguno nuevo."
fi

#gunicorn webrosters.wsgi:application  Iniciar Gunicorn (o el servidor que estés utilizando)
gunicorn webrosters.wsgi:application #--bind 0.0.0.0:8000
