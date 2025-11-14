from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    deuda = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # deuda total del cliente
    abonado = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # monto abonado

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nombre

    def total(self):
        return self.precio * self.cantidad  
    
class Movimientos(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Pendiente {self.cliente} - {self.monto}"

class PagoRecibido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='abonos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField(auto_now_add=True)
    metodo = models.CharField(max_length=100, blank=True, null=True)
    referencia = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Pago de {self.cliente}: {self.monto}"
