from django.urls import path
from . import views

urlpatterns = [
    path('turnos/', views.index_view, name='turnos_list'),
    
]
