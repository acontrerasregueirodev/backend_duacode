from django.contrib import admin
from .models import SubirArchivo

class SubirArchivoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'file', 'descripcion', 'uploaded_at')  # Campos a mostrar en la lista
    search_fields = ('titulo',)  # Permite buscar por el título del archivo
    list_filter = ('uploaded_at',)  # Filtrar por fecha de subida

admin.site.register(SubirArchivo, SubirArchivoAdmin)
