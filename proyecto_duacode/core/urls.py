from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpleadoViewset, WelcomeView
#from proyectos.views import ProyectoViewSet

router = DefaultRouter()
router.register(r'', EmpleadoViewset)  # Genera rutas como /api/empleados/

urlpatterns = [
    path('empleado/perfil/', EmpleadoViewset.as_view({'get': 'retrieve', 'put': 'update'}), name='empleado-perfil'),
    path('', include(router.urls)),
]