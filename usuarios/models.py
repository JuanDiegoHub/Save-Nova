from django.db import models

class Usuario(models.Model):
    usuario = models.CharField(max_length=50, unique=True)
    contraseña = models.CharField(max_length=255)  # Puedes dejarlo TEXT
    correo = models.EmailField(unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario
