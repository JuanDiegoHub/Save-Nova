from django.shortcuts import redirect
from usuarios.models import Usuario
from django.shortcuts import render
from usuarios.decorators import login_requerido


@login_requerido
def config_dashboard(request):
    usuario = request.usuario_actual
    return render(request, "config/dashboard.html", {"usuario": usuario})

@login_requerido
def cambiar_usuario(request):
    usuario = request.usuario_actual

    if request.method == "POST":
        nuevo_usuario = request.POST.get("usuario")

        # Validar duplicado
        if Usuario.objects.filter(usuario=nuevo_usuario).exclude(id=usuario.id).exists():
            return render(request, "config/cambiar_usuario.html", {
                "usuario": usuario,
                "error": "Ese nombre de usuario ya existe."
            })

        usuario.usuario = nuevo_usuario
        usuario.save()
        return redirect("config_dashboard")

    return render(request, "config/cambiar_usuario.html", {"usuario": usuario})

@login_requerido
def cambiar_correo(request):
    usuario = request.usuario_actual

    if request.method == "POST":
        nuevo_correo = request.POST.get("correo")
        usuario.correo = nuevo_correo
        usuario.save()
        return redirect("config_dashboard")

    return render(request, "config/cambiar_correo.html", {"usuario": usuario})

@login_requerido
def cambiar_telefono(request):
    usuario = request.usuario_actual

    if request.method == "POST":
        nuevo_tel = request.POST.get("telefono")

        if nuevo_tel == usuario.telefono:
            return render(request, "config/cambiar_telefono.html", {
                "error": "El número debe ser diferente al actual.",
                "usuario": usuario
            })

        usuario.telefono = nuevo_tel
        usuario.save()
        return redirect("config_dashboard")

    return render(request, "config/cambiar_telefono.html", {"usuario": usuario})

from django.contrib.auth.hashers import make_password, check_password

@login_requerido
def cambiar_contraseña(request):
    usuario = request.usuario_actual


    if request.method == "POST":
        actual = request.POST.get("actual", "")
        nueva = request.POST.get("nueva", "")
        confirmar = request.POST.get("confirmar", "")


        if not check_password(actual, usuario.contraseña):
            return render(request, "config/cambiar_contraseña.html", {
                "usuario": usuario,
                "error": "La contraseña actual es incorrecta."
            })


        if nueva != confirmar:
            return render(request, "config/cambiar_contraseña.html", {
                "usuario": usuario,
                "error": "La nueva contraseña y su confirmación no coinciden."
        })


        if len(nueva) < 8:
            return render(request, "config/cambiar_contraseña.html", {
            "usuario": usuario,
            "error": "La contraseña debe tener al menos 8 caracteres."
        })


        usuario.contraseña = make_password(nueva)
        usuario.save()
        return redirect("config_dashboard")


    return render(request, "config/cambiar_contraseña.html", {"usuario": usuario})