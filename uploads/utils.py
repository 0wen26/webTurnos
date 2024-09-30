import os
import re
from datetime import datetime, timedelta
import PyPDF2

def convertir_a_decimal(timedelta_obj):
    """Convierte un objeto timedelta a horas en formato decimal."""
    total_segundos = timedelta_obj.total_seconds()
    horas_decimal = total_segundos / 3600  # Convertir segundos a horas
    return round(horas_decimal, 2)  # Redondear a 2 decimales

def extraer_horas_extras(pdf_file):
    """Extraer el mes, horas extras, número de contrato y horas totales del PDF."""
    try:
        # pdf_file ya es un archivo en memoria que se puede pasar directamente a PyPDF2
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        texto_completo = ""
        
        # Extraer texto de cada página del PDF
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            texto_completo += page.extract_text() + "\n"
        
        # Definir patrones de búsqueda
        patron_fecha = re.compile(r'\d{1,2}-(\w+)\s')
        patron_horas_extra = re.compile(r'\d{2}:\d{2}\s+\d{2}:\d{2}\s+.+\(HR\)\s+(\d{2}:\d{2})')
        patron_contrato = re.compile(r'Contrato de trabajo\s*:\s*(\d{3})\.\d{5}')
        patron_horas_totales = re.compile(r'(\d{1,3}):(\d{2})\s*$')

        mes = None
        total_horas_extras = timedelta()
        contrato_numero = None
        horas_totales = None

        lineas = texto_completo.splitlines()
        for linea in lineas:
            # Extraer el mes
            match_fecha = patron_fecha.search(linea)
            if match_fecha:
                mes = match_fecha.group(1)

            # Extraer las horas extras
            match_horas_extra = patron_horas_extra.search(linea)
            if match_horas_extra:
                horas_extra = match_horas_extra.group(1)
                horas_extra_dt = datetime.strptime(horas_extra, "%H:%M")
                duracion_extra = timedelta(hours=horas_extra_dt.hour, minutes=horas_extra_dt.minute)
                total_horas_extras += duracion_extra

            # Extraer el número de contrato
            match_contrato = re.search(r'Contrato de trabajo\s*:\s*(\d+)\.\d+', linea)

            if match_contrato:
                contrato_numero = match_contrato.group(1)

            # Extraer el total de horas
            match_horas_totales = patron_horas_totales.search(linea)
            if match_horas_totales:
                horas_totales = match_horas_totales.group(0)

        total_horas_extras_decimal = convertir_a_decimal(total_horas_extras)

        if horas_totales:
            horas_totales_h, horas_totales_m = map(int, horas_totales.split(":"))
            horas_totales_timedelta = timedelta(hours=horas_totales_h, minutes=horas_totales_m)
            horas_totales_decimal = convertir_a_decimal(horas_totales_timedelta)

            if contrato_numero is not None:
                contrato_numero_decimal = int(contrato_numero)
            else:
                contrato_numero_decimal = 0  # Valor por defecto si no se encuentra

            horas_complementarias_decimal = horas_totales_decimal - contrato_numero_decimal - total_horas_extras_decimal
                        
            # Asegúrate de que horas_complementarias_decimal sea al menos 0
            horas_complementarias_decimal = max(0, round(horas_complementarias_decimal, 2))

            return {
                "mes": mes,
                "total_horas_extras_decimal": total_horas_extras_decimal,
                "contrato_numero": contrato_numero,
                "horas_totales_decimal": horas_totales_decimal,
                "horas_complementarias_decimal": horas_complementarias_decimal  # Cambiado aquí
            }
        else:
            print("No se pudo encontrar el total de horas.")
            return None
        
    except Exception as e:
        print(f"Error al procesar el archivo PDF: {e}")
        return None

