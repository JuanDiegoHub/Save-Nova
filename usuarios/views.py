from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages



def login_registro_view(request):

    # ----- SI SE ENVÍA EL FORMULARIO DE REGISTRO -----
    if request.method == "POST" and "btn_registro" in request.POST:
        usuario = request.POST.get("usuario")
        correo = request.POST.get("email")
        telefono = request.POST.get("Telefono")
        contraseña = request.POST.get("contraseña")

        if Usuario.objects.filter(usuario=usuario).exists():
            messages.warning(request, "El nombre del usuario ya está registrado.")
            return redirect('login')
        
        if Usuario.objects.filter(correo=correo).exists():
            messages.warning(request, "El correo ya se encuentra registrado.")
            return redirect('login')


        Usuario.objects.create(
            usuario=usuario,
            correo=correo,
            telefono=telefono,
            contraseña=make_password(contraseña)
        )  
        messages.success(request,"Registro existoso.")
        return redirect('login')

    # ----- SI SE ENVÍA EL FORMULARIO DE LOGIN -----

    if request.method == "POST" and "btn_login" in request.POST:
            usuario = request.POST.get("usuario")
            contraseña = request.POST.get("contraseña")

            try:
                user = Usuario.objects.get(usuario=usuario)

                if check_password(contraseña, user.contraseña):
                    
                    request.session["usuario_id"] = user.id
                    request.session["usuario_nombre"] = user.usuario

                    return redirect('menu')

                else:
                    return render(request, "usuarios/login.html", {
                        "error_login": "Usuario o contraseña incorrectos."
                    })

            except Usuario.DoesNotExist:
                return render(request, "usuarios/login.html", {
                    "error_login": "Usuario o contraseña incorrectos."
                })

    return render(request, "usuarios/login.html")