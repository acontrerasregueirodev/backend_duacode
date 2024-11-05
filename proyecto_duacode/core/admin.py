from django.contrib import admin
from .models import Empleado  # Asegúrate de importar el modelo Empleado
from .models import RolModel  # Si necesitas también manejar el modelo Rol

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_1', 'apellido_2', 'email', 'telefono', 'rol')
    search_fields = ('nombre', 'apellido_1', 'email')
    list_filter = ('rol',)
    fields = ('qr_code','nombre', 'apellido_1', 'apellido_2', 'email', 'telefono', 'fecha_contratacion', 'cumpleaños', 'is_on_leave', 'foto', 'rol', 'sede')

# Registra el modelo Empleado con su clase de administración
admin.site.register(Empleado, EmpleadoAdmin)
# Registra también el modelo RolModel si es necesario
admin.site.register(RolModel)




