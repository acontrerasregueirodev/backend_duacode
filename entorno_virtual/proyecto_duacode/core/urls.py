# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpleadoViewset
from proyectos.views import ProyectoViewSet

router = DefaultRouter()
router.register(r'empleados', EmpleadoViewset)  # Genera rutas como /api/empleados/
router.register(r'proyectos', ProyectoViewSet)  # Genera rutas como /api/proyectos/


urlpatterns = [
    path('', include(router.urls)),    
    # path('api/', include('proyectos.urls')),  # Esto incluye las rutas de proyectos sin duplicar el prefijo

]

