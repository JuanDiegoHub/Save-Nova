from django.urls import path
from . import views

urlpatterns = [
    path("crear/", views.crear_pedido, name="crear_pedido"),
    path("guardar/", views.guardar_pedido, name="guardar_pedido"),
]
