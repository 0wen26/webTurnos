from django.urls import path
from . import views
from .views import upload_overtime, delete_overtime

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('overtime/', upload_overtime, name='upload_overtime'),
    path('overtime_success/', views.overtime_success, name='overtime_success'),
    path('delete_overtime/<int:id>/', delete_overtime, name='delete_overtime'),
]
