from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):

    telefono = forms.IntegerField(
        min_value=0,
        label="Teléfono",
        error_messages={
            "invalid": "Solo se permiten números en el teléfono.",
            "required": "El teléfono es obligatorio."
        },
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Ingrese solo números"
        })
    )

    direccion = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Pon tu dirección válida"
        })
    )

    correo = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Ingresa un correo válido"
        })
    )

    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'direccion', 'correo']

