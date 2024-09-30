from django.db import models
from django.contrib.auth.models import User
# En uploads/views.py
from turnos.models import Turno  # Cambia esto si Turno no está aquí


class PDFUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona el PDF con un usuario
    file = models.FileField(upload_to='pdfs/')  # Campo para subir el archivo PDF
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Fecha de subida

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
class Overtime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mes = models.CharField(max_length=7)  # Para almacenar "YYYY-MM"
    horas_extras = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return f"{self.user} - {self.mes}: {self.horas_extras} horas extras"
    
class OvertimeData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mes = models.CharField(max_length=20)
    contrato_numero = models.CharField(max_length=20)
    total_horas_extras_decimal = models.DecimalField(max_digits=5, decimal_places=2)
    horas_complementarias_decimal = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.mes}'