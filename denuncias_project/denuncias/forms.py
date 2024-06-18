# forms.py

from django import forms
from .models import Denuncia

class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['titulo', 'descripcion', 'nombre_demandante', 'dni_demandante', 'estado', 'tipo_delito', 'barrio', 'fecha', 'documento_adjunto']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }


class LimitedDenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['estado', 'fecha']  # Campos disponibles para edición por empleados
