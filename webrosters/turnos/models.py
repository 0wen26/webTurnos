from django.db import models

class Turno(models.Model):
    fecha = models.CharField(max_length=100)
    nombre_turno = models.CharField(max_length=100)
    nombres = models.JSONField()  # Usa JSONField para almacenar una lista de nombres

    def __str__(self):
        return f"{self.fecha} - {self.nombre_turno}"
