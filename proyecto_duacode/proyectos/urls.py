# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProyectoViewSet,ProyectosPorEmpleadoView

router = DefaultRouter()
router.register(r'', ProyectoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('empleados/<int:empleado_id>/proyectos/', ProyectosPorEmpleadoView.as_view(), name='proyectos-por-empleado'),
]
