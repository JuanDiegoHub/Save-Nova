from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['usuario'],
                                password=cd['contraseña'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Autentificacíon Satisfactoria')
                else:
                    return HttpResponse('Autentificacíon Fallida')
            else:
                return HttpResponse('Usuario invalido')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})