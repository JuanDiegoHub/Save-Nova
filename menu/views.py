from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')  # redirige a la url nombrada 'login' si no está autenticado
def menu_principal(request):
    return render(request, 'menu/menu.html')