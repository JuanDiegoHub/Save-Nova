from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Producto, PagoRecibido
from .forms import ClienteForm, ProductoForm

# Página de inicio
def home(request):
    return render(request, 'usuarios/base.html')

# Lista de clientes
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'usuarios/lista_clientes.html', {'clientes': clientes})

# Agregar un nuevo cliente
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return redirect('detalle_cliente', cliente_id=cliente.id)
    else:
        form = ClienteForm()
    return render(request, 'usuarios/agregar_cliente.html', {'form': form})

# Detalle de cliente con sus productos y abonos
def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    productos = cliente.productos.all()   # Producto tiene ForeignKey a Cliente
    abonos = cliente.abonos.all()         # PagoRecibido con related_name='abonos'
    return render(request, 'usuarios/detalle_cliente.html', {
        'cliente': cliente,
        'productos': productos,
        'abonos': abonos
    })

# Agregar un producto a un cliente
def agregar_producto(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.cliente = cliente
            producto.save()

            # Actualizar deuda del cliente
            cliente.deuda += producto.total()
            cliente.save()

            return redirect('detalle_cliente', cliente_id=cliente.id)
    else:
        form = ProductoForm()

    return render(request, 'usuarios/agregar_producto.html', {
        'form': form,
        'cliente': cliente
    })

# Abonar un monto parcial
def abonar_deuda(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == "POST":
        monto = request.POST.get("monto")
        if monto:
            monto = Decimal(monto)
            cliente.abonado += monto
            cliente.deuda -= monto
            cliente.save()

            # Guardar registro del pago
            PagoRecibido.objects.create(cliente=cliente, monto=monto)

            return redirect('detalle_cliente', cliente_id=cliente.id)

    return render(request, 'usuarios/abonar_cliente.html', {'cliente': cliente})

# Pagar deuda total
def pagar_deuda_total(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == "POST":
        total = cliente.deuda
        if total > 0:
            cliente.abonado += total
            cliente.deuda = 0
            cliente.save()

            # Guardar registro del pago
            PagoRecibido.objects.create(cliente=cliente, monto=total)

        return redirect('detalle_cliente', cliente_id=cliente.id)

    return render(request, 'usuarios/pagar_deuda_total.html', {'cliente': cliente})
