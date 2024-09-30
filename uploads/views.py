import logging
logger = logging.getLogger(__name__)
import os
import PyPDF2
import re
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Turno  # Asegúrate de que Turno esté correctamente importado
from django.contrib.auth.decorators import login_required
from .models import  OvertimeData
from django.core.files.storage import FileSystemStorage
from .utils import extraer_horas_extras
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def normalize_text(text):
    """Normaliza los caracteres mal codificados en el texto."""
    #print("Texto original antes de la normalización:", text)  # Ver el texto original

    # Diccionario para mapear los caracteres incorrectos a los correctos
    character_map = {
        'PEA\'A': 'PEÑA',  # Corregir 'PEA'A' por 'PEÑA'
        'MAa': 'Mª',       # Corregir 'MAa' por 'Mª'
        'Ã‘': 'Ñ',
        'Âª': 'ª',
        'Âº': 'º',
        'Ã¡': 'á',
        'Ã©': 'é',
        'Ã­': 'í',
        'Ã³': 'ó',
        'Ãº': 'ú',
        'Ã¼': 'ü',
        'Ã€': 'À',
        'Â´': '´',
        'Æ‘': 'ñ',
        'MÂª': 'Mª',       # Caso específico de 'Mª'
        # Corrección directa de 'pea' a 'Carmen'
    }

    # Reemplazar los caracteres problemáticos utilizando el diccionario
    for bad_char, correct_char in character_map.items():
        text = text.replace(bad_char, correct_char)

    #print("Texto después de la normalización:", text)  # Ver el texto normalizado
    return text
def obtener_indice_nombre(pdf_file_name):
    """Determina el índice de extracción del nombre basado en el nombre del archivo PDF."""
    if 'Carmen' in pdf_file_name:
        return -1  # El apellido es el último
    elif 'Maro' in pdf_file_name :
        return 0   # El apellido es el primero
    elif 'Raul' in pdf_file_name or 'Isra' in pdf_file_name:
        return 2  # El apellido es el penúltimo
    else:
        return -2  # Valor por defecto
    
def extraer_datos_pdf(pdf_file_path):
    """Extraer datos estructurados del PDF."""
    datos_estructurados = []  # Inicializamos la lista vacía

    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        texto_completo = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            texto_completo += page.extract_text() + "\n"

        # **Aplicar la normalización al texto extraído**
        texto_completo = normalize_text(texto_completo)  # <--- Aquí llamamos a la función de normalización
        # Ahora podemos proceder a extraer el nombre completo de la persona
        patron_nombre = re.compile(r'Apellido\s*:\s*(.+)')

        # Después de aplicar la nueva expresión regular
        match_nombre = patron_nombre.search(texto_completo)
        if match_nombre:
            nombre_completo = match_nombre.group(1).strip()
            
            # Normalizar el texto si es necesario
            nombre_completo = normalize_text(nombre_completo)
            
            # Dividir el nombre completo en partes
            nombres = [n for n in nombre_completo.split() if len(n) > 0]

            # Si la lista contiene más de un nombre
            if len(nombres) >= 2:
                # Caso especial para "DEL CARMEN" u otros similares
                if nombres[-2].lower() == "del":
                    nombre_persona = nombres[-1].lower()  # Tomamos "CARMEN"
                else:
                    if nombres[-2].lower() == "israel" or nombres[-2].lower() == "raul":
                        # Para nombres con más de una palabra, tomamos el primero (primer nombre)
                        nombre_persona = nombres[-2].lower()  # Tomamos "Israel" en "Israel Eulises"
                    else:
                        nombre_persona = nombres[-1].lower()  # Tomamos "Israel" en "Israel Eulises"

            else:
                # Si solo hay un nombre o apellido
                nombre_persona = nombres[0].lower()  # Tomamos el único nombre disponible      

        else:
            nombre_persona = "desconocido"

        # Expresión regular para capturar el nombre del turno
        patron_turno_principal = re.compile(r'\s*([A-Za-z]{3}\d{2}-\w+)\s+\d{2}:\d{2}\s+\d{2}:\d{2}\s+([A-Z]+[\w/ ]*)\s+bcn\s+(\d{2}:\d{2})\s+(\d{2}:\d{2})')
        patron_turno_adicional = re.compile(r'\s+([A-Z]+[\w/ ]*)\s+(\d{2}:\d{2})\s+(\d{2}:\d{2})')

        lineas = texto_completo.splitlines()
        for i, linea in enumerate(lineas):
            match_principal = patron_turno_principal.search(linea)
            if match_principal:
                fecha_con_dia, nombre_turno, hora_inicio, hora_fin = match_principal.groups()

                nombre_turno = re.sub(r'\s*bcn$', '', nombre_turno, flags=re.IGNORECASE).strip()
                fecha = re.sub(r'^[A-Za-z]{3}', '', fecha_con_dia).strip()

                evento = {
                    "fecha": fecha,
                    "turno": nombre_turno,
                    "nombres": [nombre_persona]
                }
                datos_estructurados.append(evento)

                j = i + 1
                while j < len(lineas):
                    match_adicional = patron_turno_adicional.match(lineas[j])
                    if match_adicional:
                        nombre_turno_adicional, hora_inicio_adicional, hora_fin_adicional = match_adicional.groups()
                        nombre_turno_adicional = re.sub(r'\s*bcn$', '', nombre_turno_adicional, flags=re.IGNORECASE).strip()

                        evento_adicional = {
                            "fecha": fecha,
                            "turno": nombre_turno_adicional,
                            "nombres": [nombre_persona]
                        }
                        datos_estructurados.append(evento_adicional)

                        j += 1
                    else:
                        break

        return datos_estructurados
    
# Función para combinar los datos nuevos con la base de datos
def combinar_datos(datos_nuevos):
    """Combinar datos nuevos con los existentes en la base de datos"""
    for nuevo_evento in datos_nuevos:
        # Comprobar si el evento ya existe en la base de datos
        turno_existente = Turno.objects.filter(fecha=nuevo_evento['fecha'], nombre_turno=nuevo_evento['turno']).first()

        if turno_existente:
            # Si el turno ya existe, añadir los nuevos nombres si no están ya
            nombres_existentes = set(turno_existente.nombres)  # Esto debería funcionar ahora
            for nombre in nuevo_evento["nombres"]:
                if nombre not in nombres_existentes:
                    nombres_existentes.add(nombre)  # Usamos un conjunto para evitar duplicados
            turno_existente.nombres = list(nombres_existentes)  # Convertimos de nuevo a lista
            turno_existente.save()
        else:
            # Crear un nuevo objeto Turno si no existe
            Turno.objects.create(fecha=nuevo_evento['fecha'], nombre_turno=nuevo_evento['turno'], nombres=nuevo_evento['nombres'])


# Función para manejar el archivo subido
def handle_uploaded_file(f):
    file_path = os.path.join(settings.MEDIA_ROOT, f.name)

    # Guardar el archivo temporalmente
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # Procesar el archivo PDF
    datos_pdf = extraer_datos_pdf(file_path)

    # Combinar los datos con la base de datos
    combinar_datos(datos_pdf)

    # Eliminar el archivo temporal
    os.remove(file_path)

# Vista para subir el archivo PDF
# Funciones de utilidad

# Vista para subir y procesar el PDF
@login_required
def upload_overtime(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        
        # Guardar el archivo PDF utilizando la función existente
        try:
            handle_uploaded_file(pdf_file)  # Procesa y guarda el archivo
            messages.success(request, "Datos de horas extras guardados correctamente.")
            return redirect('turnos_list')
        except Exception as e:
            messages.error(request, f"Error al guardar datos: {e}")
    return render(request, 'uploads/upload_overtime.html')


@login_required
def overtime_success(request):
    # Obtener todos los datos del usuario actual
    overtime_data = OvertimeData.objects.filter(user=request.user)
    return render(request, 'uploads/overtime_success.html', {'overtime_data': overtime_data})
@login_required
def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        uploaded_file_url = fs.url(filename)

        # Extraer datos del PDF subido
        file_path = fs.path(filename)  # Obtener la ruta completa del archivo
        datos_pdf = extraer_horas_extras(file_path)

        if datos_pdf:
            # Guardar los datos extraídos en la base de datos
            
            OvertimeData.objects.create(
                user=request.user,
                mes=datos_pdf['mes'],
                contrato_numero=datos_pdf['contrato_numero'],
                total_horas_extras_decimal=datos_pdf['total_horas_extras_decimal'],
                horas_complementarias_decimal=datos_pdf['horas_complementarias_decimal']
            )
        
        # Redirigir a la página de éxito
        return redirect('overtime_success')

    return render(request, 'uploads/upload.html')

@csrf_exempt  # Si estás usando el token CSRF, asegúrate de manejarlo correctamente



@require_http_methods(["DELETE"])
@login_required
def delete_overtime(request, id):
    logger.debug(f"Solicitud DELETE recibida para eliminar OvertimeData con ID: {id} por el usuario: {request.user.username}")
    
    try:
        # Filtrar el registro por ID y usuario para asegurar que solo el propietario pueda eliminarlo
        overtime_data = OvertimeData.objects.get(id=id, user=request.user)
        overtime_data.delete()
        logger.debug(f"Registro OvertimeData con ID: {id} eliminado correctamente.")
        return JsonResponse({'message': 'Registro eliminado correctamente.'}, status=200)
    except OvertimeData.DoesNotExist:
        logger.warning(f"Registro OvertimeData con ID: {id} no encontrado o no pertenece al usuario: {request.user.username}")
        return JsonResponse({'error': 'Registro no encontrado o no tienes permiso para eliminarlo.'}, status=404)
    except Exception as e:
        logger.error(f"Error al eliminar el registro OvertimeData con ID: {id}: {str(e)}")
        return JsonResponse({'error': 'Ocurrió un error al eliminar el registro.'}, status=500)