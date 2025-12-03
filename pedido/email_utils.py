from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def enviar_correo_pedido(pedido):
    subject = f"Nuevo pedido #{pedido.id}"
    to = [pedido.cliente.correo]

    # Renderizar plantilla HTML
    html_content = render_to_string("emails/pedido_detalle.html", {"pedido": pedido})

    email = EmailMultiAlternatives(subject, "", to=to)
    email.attach_alternative(html_content, "text/html")
    email.send()
