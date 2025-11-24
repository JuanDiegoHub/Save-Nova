from .models import Usuario


def get_usuario_actual(request):
    usuario_id = request.session.get("usuario_id")
    if usuario_id is None:
        return None
    try:
        return Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return None