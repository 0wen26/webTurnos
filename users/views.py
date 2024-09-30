from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Cuenta creada exitosamente!")
            return redirect('/')  # Cambia 'home' por la vista a la que quieres redirigir después
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
