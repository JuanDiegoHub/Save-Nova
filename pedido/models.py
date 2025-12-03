# pedido/models.py

from django.db import models
from CreacionUsu.models import Cliente

class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="pedidos"
    )
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado= models.CharField(
        max_length=20,
        choices=[("Pendiente", "Pendiente"), ("Pagado", "Pagado")],
        default="Pendiente"
    )
    def actualizar_estado(self):
        pagos_total=sum(m.monto for m in self.movimientos.all())
        if pagos_total >= self.total:
            self.estado = "Pagado"
            self.save()

    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.cliente.nombre}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    nombre_producto = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre_producto} x{self.cantidad}"
    
class MovimientoPago(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="movimientos")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(
        max_length=20,
        choices=[("abono", "Abono"), ("pago_total", "Pago Total")]
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pedido.actualizar_estado()

    def __str__(self):
        return f"{self.tipo} - {self.cliente.nombre} - {self.monto}"
    
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        return self.cantidad * self.valor_unitario