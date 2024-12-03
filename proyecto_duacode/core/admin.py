from django.contrib import admin
from .models import Empleado  # Asegúrate de importar el modelo Empleado
from .models import RolModel  # Si necesitas también manejar el modelo Rol
from .forms import EmpleadoForm
class EmpleadoAdmin(admin.ModelAdmin):
    form = EmpleadoForm  # Usa el formulario personalizado para el admin

    list_display = ['id', 'nombre', 'apellido_1', 'apellido_2', 'email', 'telefono', 'rol', 'sede', 'baja', 'excedencia', 'teletrabajo', 'vacaciones']
    search_fields = ['nombre', 'apellido_1', 'apellido_2', 'email']
    list_filter = ['baja', 'excedencia', 'teletrabajo', 'vacaciones']
    
    fieldsets = (
        (None, {
            'fields': ('nombre', 'apellido_1', 'apellido_2', 'email', 'telefono', 'rol', 'sede', 'foto', 'qr_code')
        }),
        ('Estado del empleado', {
            'fields': ('baja', 'excedencia', 'teletrabajo', 'vacaciones')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Mostrar los datos antes de guardar
        print(f"Datos antes de guardar: {form.cleaned_data}")

        # Llamar al método original para guardar el objeto
        super().save_model(request, obj, form, change)
        print(f"Empleado actualizado: {obj}")

# Registra el modelo y el admin
admin.site.register(Empleado, EmpleadoAdmin)
