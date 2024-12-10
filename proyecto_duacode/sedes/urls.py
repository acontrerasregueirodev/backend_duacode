from rest_framework import routers
from django.urls import path

#from .views import SedeViewSet, SalaReunionesViewSet, ReservaSalaViewSet
from .views import ReservaSalaViewSet, SedeViewSet, SalaReunionesViewSet,ReunionesPorSedeView
router = routers.DefaultRouter()
# router.register(r'sedes', SedeViewSet)
# router.register(r'salas', SalaReunionesViewSet)
router.register(r'reservas', ReservaSalaViewSet)
router.register(r'sedes', SedeViewSet)
router.register(r'salas', SalaReunionesViewSet)
# Rutas adicionales
urlpatterns = router.urls + [
    path('api/reuniones_por_sede/', ReunionesPorSedeView.as_view(), name='reuniones-por-sede'),
]