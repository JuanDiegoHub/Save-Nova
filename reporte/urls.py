from django.urls import path
from . import views

urlpatterns = [
    path("informe/", views.informe_mensual, name="informe_mensual"),
    path("reporte/pdf/", views.generar_reporte_pdf, name="generar_reporte_pdf"),
]
