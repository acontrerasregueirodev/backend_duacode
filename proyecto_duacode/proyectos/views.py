# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Proyecto
from .serializers import ProyectoSerializer
from rest_framework.permissions import IsAuthenticated

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación

    @action(detail=True, methods=['delete'])
    def eliminar_proyecto(self, request, pk=None):
        proyecto = get_object_or_404(Proyecto, pk=pk)
        proyecto.delete()
        return Response({'message': 'Proyecto eliminado exitosamente'}, status=status.HTTP_200_OK)
