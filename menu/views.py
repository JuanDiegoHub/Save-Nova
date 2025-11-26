from django.shortcuts import render, redirect, get_object_or_404
from pedido.models import Pedido

# Vista principal que muestra los pedidos en tarjetas
def menu(request):
    pedidos = Pedido.objects.all()
    return render(request, "menu/menu.html", {"pedidos": pedidos})

