from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from pedido.models import Pedido
import datetime
from django.utils.dateparse import parse_date
from django.utils.timezone import now
import pandas as pd
from pedido.models import Pedido, MovimientoPago
from CreacionUsu.models import Cliente
from django.db.models import Sum
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



def reporte_rango_fechas(request):
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")
    cliente_id = request.GET.get("cliente_id", "")

    pedidos = Pedido.objects.all()

    # FILTRAR FECHAS
    if fecha_inicio and fecha_fin:
        pedidos = pedidos.filter(
            fecha_pedido__date__gte=fecha_inicio,
            fecha_pedido__date__lte=fecha_fin
        )

    # FILTRAR POR CLIENTE
    if cliente_id and cliente_id != "0":
        pedidos = pedidos.filter(cliente_id=cliente_id)

    clientes = Cliente.objects.all()

    movimientos_list = []

    for pedido in pedidos:
        movimientos = MovimientoPago.objects.filter(pedido=pedido).order_by("fecha")

        acumulado = 0
        for m in movimientos:
            acumulado += m.monto
            saldo_restante = pedido.total - acumulado

            movimientos_list.append({
                "cliente": pedido.cliente.nombre,
                "fecha": m.fecha,
                "abono": m.monto,
                "saldo": saldo_restante,
                "estado": "Pagado" if saldo_restante <= 0 else "Pendiente"
            })

    return render(request, "reporte/informe_mensual.html", {
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "cliente_id": cliente_id,
        "clientes": clientes,
        "movimientos": movimientos_list,
    })


def exportar_excel_pedidos(request):
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    pedidos = Pedido.objects.all()

    if fecha_inicio and fecha_fin:
        pedidos = pedidos.filter(
            fecha_pedido__date__range=[fecha_inicio, fecha_fin]
        )

    # Construimos el DataFrame
    data = []
    for p in pedidos:
        data.append({
            "ID Pedido": p.id_pedido,
            "Cliente": p.cliente.nombre,
            "Fecha del pedido": p.fecha_pedido.strftime("%Y-%m-%d %H:%M:%S"),
            "Total": float(p.total),
            "Estado": p.estado,
        })

    df = pd.DataFrame(data)

    # Configuración de la respuesta
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    nombre_archivo = f"Reporte_{fecha_inicio}_a_{fecha_fin}.xlsx"
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'

    # Crear archivo Excel con XlsxWriter
    with pd.ExcelWriter(response, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Pedidos", index=False)

        workbook = writer.book
        worksheet = writer.sheets["Pedidos"]

        # Formato del encabezado
        formato_header = workbook.add_format({
            "bold": True,
            "bg_color": "#DDEBF7",
            "border": 1
        })
        worksheet.set_row(0, None, formato_header)

        worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)

    return response

def informe_mensual(request):
    fecha = request.GET.get("fecha")  # formato YYYY-MM

    pedidos = Pedido.objects.none()
    year = None
    month = None

    if fecha:
        year, month = fecha.split("-")
        year = int(year)
        month = int(month)

        pedidos = Pedido.objects.filter(
            fecha_pedido__year=year,
            fecha_pedido__month=month
        )

    # 🔥 AGREGAR ESTO PARA ENVIAR CLIENTES AL TEMPLATE
    clientes = Cliente.objects.all()

    return render(request, "reporte/informe_mensual.html", {
        "pedidos": pedidos,
        "year": year,
        "month": month,
        "fecha": fecha,
        "clientes": clientes,   # 👈 ahora sí llegan al template
    })



def reporte_cliente(request):
    cliente_id = request.GET.get("cliente")

    clientes = Cliente.objects.all().order_by("nombre")
    movimientos_data = []
    pedido_seleccionado = None

    if cliente_id:
        # Obtener pedidos del cliente
        pedidos = Pedido.objects.filter(cliente_id=cliente_id).order_by("-fecha_pedido")

        if pedidos.exists():
            pedido_seleccionado = pedidos.first()
            total_restante = float(pedido_seleccionado.total)

            # Movimientos ordenados por fecha ascendente
            movimientos = MovimientoPago.objects.filter(
                pedido=pedido_seleccionado
            ).order_by("fecha")

            for m in movimientos:
                total_restante -= float(m.monto)

                movimientos_data.append({
                    "fecha": m.fecha,
                    "abono": m.monto,
                    "total_despues": total_restante,
                    "estado": pedido_seleccionado.estado
                })

    return render(request, "reporte/reporte_cliente.html", {
        "clientes": clientes,
        "movimientos": movimientos_data,
        "pedido": pedido_seleccionado,
        "cliente_id": cliente_id,
    })
def reporte_movimientos_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id_pedido=pedido_id)
    movimientos = pedido.movimientos.order_by("fecha")

    historial = []
    saldo = pedido.total  # Total inicial del pedido

    # 1. Fila inicial del pedido
    historial.append({
        "cliente": pedido.cliente.nombre,
        "fecha": pedido.fecha_pedido,
        "abono": 0,
        "saldo": saldo,
        "estado": "Pendiente" if saldo > 0 else "Pagado",
        "descripcion": "Creación del pedido"
    })

    # 2. Recorrer los abonos
    for mov in movimientos:
        saldo -= mov.monto
        historial.append({
            "cliente": pedido.cliente.nombre,
            "fecha": mov.fecha,
            "abono": mov.monto,
            "saldo": saldo,
            "estado": "Pagado" if saldo <= 0 else "Pendiente",
            "descripcion": mov.tipo.replace("_", " ").capitalize()
        })

    return render(request, "reporte/movimientos.html", {"pedido": pedido, "historial": historial})
