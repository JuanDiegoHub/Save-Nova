# pedido/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal
from CreacionUsu.models import Cliente
from .models import Pedido, DetallePedido, MovimientoPago
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.apps import AppConfig

def crear_pedido(request):
    clientes = Cliente.objects.all().order_by("nombre")  
    return render(request, "pedido/crear_pedido.html", {
        "clientes": clientes
    })


@csrf_exempt
def guardar_pedido(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
        cliente_id = data.get("cliente_id")
        productos = data.get("productos", [])

        if not cliente_id:
            return JsonResponse({"error": "Debe seleccionar un cliente"}, status=400)

        if not productos:
            return JsonResponse({"error": "Debe agregar al menos un producto"}, status=400)

        cliente = Cliente.objects.get(id_cliente=cliente_id)

        # Calcular total
        total_pedido = sum(
            Decimal(str(p["cantidad"])) * Decimal(str(p["precio"]))
            for p in productos
        )

        pedido = Pedido.objects.create(
            cliente=cliente,
            total=total_pedido
        )

        # Guardar detalles
        for p in productos:
            precio_decimal = Decimal(str(p["precio"]))
            subtotal_decimal = Decimal(str(p["cantidad"])) * precio_decimal

            DetallePedido.objects.create(
                pedido=pedido,
                nombre_producto=p["nombre"],
                cantidad=p["cantidad"],
                precio=precio_decimal,
                subtotal=subtotal_decimal
            )

        # ------------------------------
        # 🔥 ENVIAR CORREO AQUÍ 🔥
        # ------------------------------
        detalles = DetallePedido.objects.filter(pedido=pedido)

        html_content = render_to_string("pedido/pedido_detalle.html", {
            "pedido": pedido,
            "detalles": detalles
        })

        email = EmailMultiAlternatives(
            subject=f"Confirmación de Pedido #{pedido.id_pedido}",
            body="Tu cliente no ve este texto si usa HTML.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[cliente.correo],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()


        
        # ------------------------------

        return JsonResponse({"success": True, "pedido_id": pedido.id_pedido})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    

def abonar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    abono = Decimal(request.POST.get("abono", "0"))

    MovimientoPago.objects.create(
        pedido=pedido,
        cliente=pedido.cliente,
        monto=abono,
        tipo="abono"
    )

    pedido.total -= abono
    if pedido.total < 0:
        pedido.total = 0
    pedido.save()

    
    if pedido.total == 0:
        pedido.estado= "Pagado"
        pedido.save()

    return redirect("menu")

def pagar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)

    MovimientoPago.objects.create(
        pedido=pedido,
        cliente=pedido.cliente,
        monto=pedido.total,  # Decimal OK
        tipo="pago_total"
    )
    pedido.total = 0
    pedido.estado = "Pagado"
    pedido.save()

    return redirect("menu")


class PedidoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pedido'

    def ready(self):
        import pedido.signals


def detalle_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)

    detalles = DetallePedido.objects.filter(pedido=pedido)

    total = sum(d.subtotal for d in detalles)

    return render(request, "pedido/detalle_pedido.html", {
        "pedido": pedido,
        "detalles": detalles,
        "total": total
    })
from django.views.decorators.http import require_POST

@require_POST
def editar_producto(request, id_detalle):
    detalle = get_object_or_404(DetallePedido, id=id_detalle)

    nombre = request.POST.get("nombre")
    cantidad = int(request.POST.get("cantidad"))
    precio = Decimal(request.POST.get("precio"))

    detalle.nombre_producto = nombre
    detalle.cantidad = cantidad
    detalle.precio = precio
    detalle.subtotal = cantidad * precio
    detalle.save()

    # recalcular total del pedido
    pedido = detalle.pedido
    total = sum(d.subtotal for d in pedido.detalles.all())
    pedido.total = total
    pedido.save()

    return JsonResponse({
        "success": True,
        "subtotal": detalle.subtotal,
        "total_pedido": pedido.total
    })


@require_POST
def eliminar_producto(request, id_detalle):
    detalle = get_object_or_404(DetallePedido, id=id_detalle)
    pedido = detalle.pedido

    detalle.delete()

    total = sum(d.subtotal for d in pedido.detalles.all())
    pedido.total = total
    pedido.save()

    return JsonResponse({
        "success": True,
        "total_pedido": pedido.total
    })
from django.views.decorators.http import require_POST
import json
from decimal import Decimal

@require_POST
def agregar_productos(request, id_pedido):

    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)

    data = json.loads(request.body)
    productos = data.get("productos", [])

    for p in productos:

        nombre = p.get("nombre")
        cantidad = int(p.get("cantidad", 0))
        precio = Decimal(str(p.get("precio", 0)))

        if nombre and precio > 0:

            subtotal = cantidad * precio

            DetallePedido.objects.create(
                pedido=pedido,
                nombre_producto=nombre,
                cantidad=cantidad,
                precio=precio,
                subtotal=subtotal
            )

    # recalcular total del pedido
    total = sum(d.subtotal for d in pedido.detalles.all())
    pedido.total = total
    pedido.save()

    return JsonResponse({
        "success": True
    })

from django.http import JsonResponse
from .models import Pedido

def cancelar_pedido(request, id_pedido):

    if request.method == "POST":

        pedido = Pedido.objects.get(id_pedido=id_pedido)

        pedido.estado = "Cancelado"
        pedido.save()

        return JsonResponse({"success": True})