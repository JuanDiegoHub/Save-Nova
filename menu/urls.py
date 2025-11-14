from django.urls import path
from .views import menu_principal

urlpatterns = [
    path('', menu_principal, name='menu'),
]
