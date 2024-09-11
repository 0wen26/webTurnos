from django.urls import path
from . import views

urlpatterns = [
    path('', views.turnos_view, name='turnos_list'),
]
