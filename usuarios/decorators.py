from django.shortcuts import redirect
from usuarios.models import Usuario

def login_requerido(func):
    def wrapper(request, *args, **kwargs):
        usuario_id = request.session.get("usuario_id")
        if usuario_id is None:
            return redirect("login")
        request.usuario_actual = Usuario.objects.get(id=usuario_id)
        return func(request, *args, **kwargs)
    return wrapper
