# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_proyectos, name='listar_proyectos'),  # Ruta para listar proyectos
    path('<int:proyecto_id>/eliminar/', views.eliminar_proyecto, name='eliminar_proyecto'),  # Ruta para eliminar proyectos
]