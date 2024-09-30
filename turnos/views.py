from django.shortcuts import render
from .models import Turno

<<<<<<< HEAD
#def index_view(request):
 #   turnos = Turno.objects.all()
  #  return render(request, 'turnos/turnos_list.html', {'turnos': turnos})

def index_view(request):
    turnos = Turno.objects.all()

    # Convertir nombres a cadenas de texto separadas por comas si no usas la propiedad en el modelo
    for turno in turnos:
        turno.nombres = ', '.join(turno.nombres)

    return render(request, 'turnos/turnos_list.html', {'turnos': turnos})
=======
def index_view(request):
    turnos = Turno.objects.all()
    return render(request, 'turnos/turnos_list.html', {'turnos': turnos})
>>>>>>> 0dcc02eede6832752b4e272e7bff5099fbdda611
