from django.shortcuts import render
from pedido.models import Pedido

def menu(request):
    q = request.GET.get("q")  # parámetro de búsqueda
    if q:
        pedidos = Pedido.objects.filter(cliente__nombre__icontains=q)
    else:
        pedidos = Pedido.objects.all()
    return render(request, "menu/menu.html", {"pedidos": pedidos, "q": q})
