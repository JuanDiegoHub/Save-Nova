from django.shortcuts import render
from pedido.models import Pedido, DetallePedido

def menu(request):
    q = request.GET.get("q")

    if q:
        pedidos = Pedido.objects.filter(cliente__nombre__icontains=q, estado="Pendiente")
    else:
        pedidos = Pedido.objects.filter(estado="Pendiente")

    for pedido in pedidos:
        pedido.productos = DetallePedido.objects.filter(pedido=pedido)

    return render(request, "menu/menu.html", {"pedidos": pedidos, "q": q})