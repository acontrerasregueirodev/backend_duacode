from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpleadoViewset, PanelEmpleadosView
from proyectos.views import ProyectoViewSet

router = DefaultRouter()
router.register(r'', EmpleadoViewset)  # Genera rutas como /api/empleados/


urlpatterns = [
    path('', include(router.urls)), 
    path('empleado/perfil/', EmpleadoViewset.as_view({'get': 'retrieve', 'put': 'update'}), name='empleado-perfil'),
    path('panel-empleados/', PanelEmpleadosView.as_view({'get': 'list'}), name='panel-empleados'),
    # path('api/', include('proyectos.urls')),  # Esto incluye las rutas de proyectos sin duplicar el prefijo
]

