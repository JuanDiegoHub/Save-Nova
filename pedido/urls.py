from django.urls import path
from . import views

urlpatterns = [
    path("crear/", views.crear_pedido, name="crear_pedido"),
    path("guardar/", views.guardar_pedido, name="guardar_pedido"),
    path('abonar/<int:id_pedido>/', views.abonar_pedido, name='abonar_pedido'),
    path('pagar/<int:id_pedido>/', views.pagar_pedido, name='pagar_pedido'),
    path('detalle/<int:id_pedido>/', views.detalle_pedido, name='detalle_pedido'),
    path('editar-producto/<int:id_detalle>/', views.editar_producto, name='editar_producto'),
    path('eliminar-producto/<int:id_detalle>/', views.eliminar_producto, name='eliminar_producto'),
    path('agregar-productos/<int:id_pedido>/', views.agregar_productos, name='agregar_productos'),
    path("cancelar-pedido/<int:id_pedido>/", views.cancelar_pedido, name="cancelar_pedido"),
]

