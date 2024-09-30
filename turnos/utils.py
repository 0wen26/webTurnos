from .models import Turno
from PyPDF2 import PdfReader

def procesar_pdf_y_actualizar_bd(pdf_file_path):
    datos = extraer_datos_pdf(pdf_file_path)
    actualizar_bd_con_datos(datos)

def extraer_datos_pdf(pdf_file_path):
    datos_estructurados = []

    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        texto_completo = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            texto_completo += page.extract_text() + "\n"

        # Aquí usas tu lógica existente para extraer los datos
        # Extraer datos y procesar...

    return datos_estructurados

def actualizar_bd_con_datos(datos):
    for item in datos:
        fecha = item['fecha']
        nombre_turno = item['turno']
        nombres = item['nombres']
        
        # Guardar en la base de datos
        Turno.objects.create(fecha=fecha, nombre_turno=nombre_turno, nombres=nombres)
