from django.urls import path
from .views import login_registro_view

urlpatterns = [
    path('', login_registro_view, name='login'),
]
