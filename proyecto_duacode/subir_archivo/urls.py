from django.urls import path
from .views import UploadFile

urlpatterns = [
    path('', UploadFile.as_view(), name='UploadFile'),  # Ruta para la página de carga
]
