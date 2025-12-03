from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.db import transaction
from .models import Pedido, DetallePedido

@receiver(post_save, sender=Pedido)
def enviar_correo_pedido(sender, instance, created, **kwargs):
    if not created:
        return

    cliente = instance.cliente
    if not cliente.correo:
        return

    # Ejecutar el envío SOLO después de que todo el pedido (incluyendo detalles) se haya guardado
    def enviar():
        detalles = DetallePedido.objects.filter(pedido=instance)

        html_content = render_to_string("pedido/pedido_detalle.html", {
            "pedido": instance,
            "detalles": detalles
        })

        email = EmailMultiAlternatives(
            subject=f"Confirmación de Pedido #{instance.id_pedido}",
            body="Tu cliente no puede ver este texto si usa HTML.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[cliente.correo],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()
        print("⚡ Correo enviado con detalles correctamente")

    transaction.on_commit(enviar)
