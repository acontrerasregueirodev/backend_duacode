# Create your views here.
from rest_framework import viewsets
from .models import Proyecto
from .serializers import ProyectoSerializer
from core.views  import BasePermisos


class ProyectoViewSet(BasePermisos):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer