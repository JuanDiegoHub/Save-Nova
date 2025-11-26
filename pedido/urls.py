from django.urls import path
from . import views

urlpatterns = [
    path("crear/", views.crear_pedido, name="crear_pedido"),
    path("guardar/", views.guardar_pedido, name="guardar_pedido"),
    path('abonar/<int:id_pedido>/', views.abonar_pedido, name='abonar_pedido'),
    path('pagar/<int:id_pedido>/', views.pagar_pedido, name='pagar_pedido'),
]
