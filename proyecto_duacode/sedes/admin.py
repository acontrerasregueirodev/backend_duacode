# admin.py en la aplicación 'sedes'

from django.contrib import admin
from .models import Sede, SalaReuniones, ReservaSala
# from .serializers import ReservaSalaSerializer, SalaReunionesSerializer
@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion')  # Campos a mostrar en la lista
    search_fields = ('nombre',)  # Campo por el que se puede buscar

@admin.register(SalaReuniones)
class SalaReunionesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'capacidad', 'sede')  # Campos a mostrar en la lista
    search_fields = ('nombre', 'sede__nombre')  # Busca por nombre de sala o sede

# class ReservaSalaAdmin(admin.ModelAdmin):
#     list_display = ('id', 'sala', 'reservado_por', 'fecha', 'hora_inicio', 'hora_fin', 'motivo')
#     search_fields = ('sala__nombre', 'reservado_por__nombre', 'motivo')  # Agregar búsqueda por sala, empleado y motivo
#     list_filter = ('fecha', 'sala')  # Filtros rápidos por fecha y sala
#     ordering = ('fecha', 'hora_inicio')  # Ordenar las reservas por fecha y hora de inicio
#     filter_horizontal = ('empleados_asistentes',)  # Hacer que el campo empleados_asistentes sea más fácil de manejar

#     # Mostrar empleados asistentes en el formulario de creación de la reserva
#     fieldsets = (
#         (None, {
#             'fields': ('sala', 'reservado_por', 'fecha', 'hora_inicio', 'hora_fin', 'motivo', 'empleados_asistentes')
#         }),
#     )

# Registrar el modelo en el admin usando el decorador correctamente
@admin.register(ReservaSala)
class ReservaSalaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sala', 'reservado_por', 'fecha', 'hora_inicio', 'hora_fin', 'motivo')
    search_fields = ('sala__nombre', 'reservado_por__nombre', 'motivo')
    list_filter = ('fecha', 'sala')
    ordering = ('fecha', 'hora_inicio')
    filter_horizontal = ('empleados_asistentes',)

    fieldsets = (
        (None, {
            'fields': ('sala', 'reservado_por', 'fecha', 'hora_inicio', 'hora_fin', 'motivo', 'empleados_asistentes')
        }),
    )