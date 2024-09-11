import json
from .models import Turno

def cargar_datos_desde_json():
    with open(r'C:\Users\spy_o\Desktop\python\datos_eventos.json', 'r', encoding='utf-8') as file:
    # código para cargar los datos

        datos = json.load(file)

        for item in datos:
            fecha = item['fecha']
            nombre_turno = item['turno']
            nombres = ', '.join(item['nombres'])  # Unimos la lista de nombres en una cadena separada por comas

            # Crear y guardar el objeto Turno en la base de datos
            Turno.objects.create(fecha=fecha, nombre_turno=nombre_turno, nombres=nombres)
