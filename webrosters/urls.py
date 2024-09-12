from django.contrib import admin
from django.urls import path, include
from turnos.views import index_view  # Asegúrate de que el nombre coincide con tu vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),  # Asegúrate de que el nombre de la vista es correcto
]
