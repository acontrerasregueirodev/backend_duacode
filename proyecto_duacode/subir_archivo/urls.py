from django.urls import path
from .views import Upload_File

urlpatterns = [
    path('', Upload_File.as_view, name='Upload_File'),  # Ruta para la página de carga
]
