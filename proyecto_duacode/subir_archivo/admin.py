from django.contrib import admin
from .models import SubirArchivo

class SubirArchivoAdmin(admin.ModelAdmin):
    list_display = ('archivo', 'descripcion', 'fecha_subida')  # Muestra el archivo, descripción y fecha subida

admin.site.register(SubirArchivo, SubirArchivoAdmin)