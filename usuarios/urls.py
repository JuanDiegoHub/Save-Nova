from django.urls import path
from . import views  # asegúrate de importar desde el punto actual (.)


urlpatterns = [
    path('',views.user_login, name='login'),
]
