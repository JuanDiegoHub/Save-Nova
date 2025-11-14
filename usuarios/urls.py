from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('', views.lista_clientes, name='lista_clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('clientes/<int:cliente_id>/productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('clientes/<int:cliente_id>/abonar/', views.abonar_deuda, name='abonar_deuda'),
    path('clientes/<int:cliente_id>/pagar/', views.pagar_deuda_total, name='pagar_deuda_total'),
]