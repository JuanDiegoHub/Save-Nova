from django.urls import path
from . import views

urlpatterns = [
    path("informe/", views.informe_mensual, name="informe_mensual"),
    path("reporte/pdf/", views.generar_reporte_pdf, name="generar_reporte_pdf"),
    path("reporte-rango/", views.reporte_rango_fechas, name="reporte_rango_fechas"),
    path("reporte-rango/excel/", views.exportar_excel_pedidos, name="exportar_excel_pedidos"),
    path("cliente/", views.reporte_cliente, name="reporte_cliente"),

]
