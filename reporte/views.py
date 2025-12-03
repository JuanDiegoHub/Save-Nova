from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from pedido.models import Pedido
from django.utils.timezone import now
import datetime
def generar_reporte_pdf(request):
    # Capturamos las fechas desde el formulario
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    pedidos = Pedido.objects.all()

    if fecha_inicio and fecha_fin:
        # Convertimos a objetos datetime
        fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")

        # Filtramos pedidos entre esas fechas
        pedidos = Pedido.objects.filter(
            fecha_pedido__range=[fecha_inicio, fecha_fin]
        ).prefetch_related("movimientos", "detalles")

    context = {
        "pedidos": pedidos,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    }

    # Renderizar HTML
    template = get_template("reporte/reporte_mensual.html")
    html = template.render(context)

    # Exportar a PDF
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
