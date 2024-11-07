# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Proyecto
from .serializers import ProyectoSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
        # Método para definir permisos según la acción
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]  # Requiere autenticación para crear, actualizar y eliminar
        return [AllowAny()]  # Permite acceso a GET sin autenticación

    @action(detail=True, methods=['delete'])
    def eliminar_proyecto(self, request, pk=None):
        proyecto = get_object_or_404(Proyecto, pk=pk)
        proyecto.delete()
        return Response({'message': 'Proyecto eliminado exitosamente'}, status=status.HTTP_200_OK)


     # Overriding the update method to handle editing a project
    def update(self, request, *args, **kwargs):
        # Retrieve the project object
        proyecto = self.get_object()

        # Serialize the request data and validate
        serializer = self.get_serializer(proyecto, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            # Save the updated project
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If validation fails, return an error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)