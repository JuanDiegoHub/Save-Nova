from django import forms
from .models import Cliente, Producto, Movimientos, PagoRecibido

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'email']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'cantidad']

class PagoRecibidoForm(forms.ModelForm):
    class Meta:
        model = PagoRecibido
        fields = ['cliente', 'monto', 'metodo', 'referencia']


class MovimientosForm(forms.ModelForm):
    class Meta:
        model = Movimientos
        fields = ['cliente', 'monto', 'fecha_vencimiento', 'descripcion']
