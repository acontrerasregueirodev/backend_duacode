# admin.py en la aplicación 'sedes'

from django.contrib import admin
from .models import Sede, SalaReuniones, ReservaSala

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion')  # Campos a mostrar en la lista
    search_fields = ('nombre',)  # Campo por el que se puede buscar

@admin.register(SalaReuniones)
class SalaReunionesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'capacidad', 'sede')  # Campos a mostrar en la lista
    search_fields = ('nombre', 'sede__nombre')  # Busca por nombre de sala o sede

@admin.register(ReservaSala)
class ReservaSalaAdmin(admin.ModelAdmin):
    list_display = ('sala', 'reservado_por', 'fecha', 'hora_inicio', 'hora_fin')
    list_filter = ('fecha',)  # Utiliza el campo 'fecha' en lugar de 'fecha_inicio'

