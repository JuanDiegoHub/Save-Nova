# pedido/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal

from CreacionUsu.models import Cliente
from .models import Pedido, DetallePedido


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

        # Calcular total correctamente
        total_pedido = sum(
            Decimal(str(p["cantidad"])) * Decimal(str(p["precio"]))
            for p in productos
        )

        pedido = Pedido.objects.create(
            cliente=cliente,
            total=total_pedido
        )

        # Guardar detalles del pedido
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

        return JsonResponse({"success": True, "pedido_id": pedido.id_pedido})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)