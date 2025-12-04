from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from pedido.models import Pedido
from django.utils.timezone import now
import datetime

def generar_reporte_pdf(request):

    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    pedidos = Pedido.objects.none()  # por defecto vacío

    if fecha_inicio and fecha_fin:
        # Convertimos fechas
        fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")

        # Para incluir TODO el día final, añadimos 23:59:59
        fecha_fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d") + datetime.timedelta(days=1)

        # Filtrar pedidos por rango de fechas
        pedidos = Pedido.objects.filter(
            fecha_pedido__range=[fecha_inicio, fecha_fin]
        ).prefetch_related("movimientos", "detalles")

    context = {
        "pedidos": pedidos,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "month": fecha_inicio.month if fecha_inicio else "",
        "year": fecha_inicio.year if fecha_inicio else "",
    }

    template = get_template("reporte/reporte_mensual.html")
    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=reporte.pdf"
    pisa.CreatePDF(html, dest=response)

    return response

def informe_mensual(request):
    actual = now()
    year = actual.year
    mes_actual = actual.month

    import calendar
    meses = []
    for i in range(1, 13):
        nombre = calendar.month_name[i].capitalize()
        bloqueado = i > mes_actual
        meses.append({
            "nombre": nombre,
            "numero": i,
            "year": year,
            "bloqueado": bloqueado
        })

    return render(request, "reporte/informe_mensual.html", {"meses": meses})
