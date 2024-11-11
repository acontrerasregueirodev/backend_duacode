from rest_framework import routers
#from .views import SedeViewSet, SalaReunionesViewSet, ReservaSalaViewSet
from .views import ReservaSalaViewSet, SedeViewSet
router = routers.DefaultRouter()
# router.register(r'sedes', SedeViewSet)
# router.register(r'salas', SalaReunionesViewSet)
router.register(r'reservas', ReservaSalaViewSet)
router.register(r'sedes', SedeViewSet)
urlpatterns = router.urls
