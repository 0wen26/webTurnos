from django.shortcuts import render
from .models import Turno

def index_view(request):
    turnos = Turno.objects.all()
    return render(request, 'turnos/turnos_list.html', {'turnos': turnos})
