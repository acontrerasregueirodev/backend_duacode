from django.urls import path
from . import views

urlpatterns = [
    path('generar/', views.generar_qr, name='generar_qr'),
    # path('leer_qr/', views.leer_qr, name='leer_qr'),
    path('scan/', views.scan, name='scan'),  # La ruta coincide con '/qr/scan/'

]
