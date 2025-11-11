from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login, logout
from .forms import LoginForm

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd.get('username'),
                                password=cd.get('password'))
            print("authenticate returned:", user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('menu_principal')
                else:
                    return render(request, 'usuarios/login.html', {'form': form, 'error': 'Cuenta inactiva'})
            else:
                return render(request, 'usuarios/login.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')
