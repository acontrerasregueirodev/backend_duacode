from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EmpleadoViewset, RolViewSet

router = DefaultRouter()

# Rutas para empleados
router.register(r'empleados', EmpleadoViewset)

# Rutas para roles
router.register(r'roles', RolViewSet, basename='roles')

urlpatterns = [
    path('', include(router.urls)),  # Incluir las rutas de todos los viewsets
]