from django import forms
from .models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'  # O puedes especificar los campos que deseas mostrar, por ejemplo: ('nombre', 'email', 'telefono', 'rol')
