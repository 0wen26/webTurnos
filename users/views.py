from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm
import logging

logger = logging.getLogger(__name__)

def register(request):
    try:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "¡Cuenta creada exitosamente!")
                return redirect('/')
            else:
                messages.error(request, "Error en el registro. Verifica los campos.")
                print("Errores en el formulario:", form.errors)  # Esto debería imprimir errores
        else:
            form = UserRegisterForm()
            print("Formulario en la vista de registro")  # Esto verifica que la vista está siendo accedida
        return render(request, 'users/register.html', {'form': form})
    except Exception as e:
        print(f"Error durante el registro: {str(e)}")


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "¡Inicio de sesión exitoso!")
            return redirect('/')
        else:
            messages.error(request, "Error en el inicio de sesión. Verifica tus credenciales.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

