from django.shortcuts import render, redirect
from .models import Usuario

def login_registro_view(request):

    # ----- SI SE ENVÍA EL FORMULARIO DE REGISTRO -----
    if request.method == "POST" and "btn_registro" in request.POST:
        usuario = request.POST.get("usuario")
        correo = request.POST.get("email")
        telefono = request.POST.get("Telefono")
        contraseña = request.POST.get("contraseña")

        Usuario.objects.create(
            usuario=usuario,
            correo=correo,
            telefono=telefono,
            contraseña=contraseña
        )

        return redirect('login')  # vuelve al login

    # ----- SI SE ENVÍA EL FORMULARIO DE LOGIN -----
    if request.method == "POST" and "btn_login" in request.POST:
        usuario = request.POST.get("usuario")
        contraseña = request.POST.get("contraseña")

        # validar usuario
        try:
            user = Usuario.objects.get(usuario=usuario, contraseña=contraseña)
            return redirect('menu')  # si el login es exitoso
        except Usuario.DoesNotExist:
            return render(request, "usuarios/login.html", {
                "error_login": "Usuario o contraseña incorrectos."
            })

    return render(request, "usuarios/login.html")
