from django.contrib import admin
from django.urls import path, include
from turnos.views import index_view  # Asegúrate de que el nombre coincide con tu vista
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),  # Asegúrate de que el nombre de la vista es correcto
    path('users/', include('users.urls')),
    path('uploads/', include('uploads.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('turnos/', include('turnos.urls')),  # Incluir URLs de turnos    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
