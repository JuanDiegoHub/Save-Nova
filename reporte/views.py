from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from pedido.models import Pedido
from django.utils.timezone import now
import calendar
def generar_reporte_pdf(request):
    hoy = now()
    # Si el usuario selecciona un mes, úsalo; si no, usa el actual
    month = int(request.GET.get("month", hoy.month))
    year = int(request.GET.get("year", hoy.year))

    pedidos = Pedido.objects.filter(
        fecha_pedido__year=year,
        fecha_pedido__month=month
    ).prefetch_related("movimientos", "detalles")

    context = {"pedidos": pedidos, "month": month, "year": year}

    # Renderizar HTML
    template = get_template("reporte/reporte_mensual.html")
    html = template.render(context)

    # Exportar a PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=reporte_{year}_{month}.pdf"
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
