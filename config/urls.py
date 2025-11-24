from django.urls import path
from . import views

urlpatterns = [
    path('', views.config_dashboard, name='config_dashboard'),

    path('cambiar-usuario/', views.cambiar_usuario, name='cambiar_usuario'),
    path('cambiar-correo/', views.cambiar_correo, name='cambiar_correo'),
    path('cambiar-telefono/', views.cambiar_telefono, name='cambiar_telefono'),
    path('cambiar-contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),
]
