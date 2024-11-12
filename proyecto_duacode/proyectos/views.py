# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Proyecto
from core.models import Empleado
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

# Acción para eliminar el proyecto
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])  # Asegurando autenticación aquí también
    def eliminar_proyecto(self, request, pk=None):
        # Verificar si el usuario está autenticado antes de proceder
        if not request.user.is_authenticated:
            raise PermissionDenied("No tienes permiso para realizar esta acción.")

        proyecto = get_object_or_404(Proyecto, pk=pk)
        proyecto.delete()
        return Response({'message': 'Proyecto eliminado exitosamente'}, status=status.HTTP_200_OK)


        # Sobrescribir el método update para manejar la relación ManyToMany
    def update(self, request, *args, **kwargs):
        # Recuperar el objeto Proyecto a editar
        proyecto = self.get_object()

        # Serializar los datos recibidos
        serializer = self.get_serializer(proyecto, data=request.data, partial=True)

        if serializer.is_valid():
            # Guardar el proyecto (esto guardará la información básica del proyecto)
            proyecto = serializer.save()

            # Ahora, actualizamos la relación ManyToMany de empleados
            if 'empleados' in request.data:
                # Recuperar los IDs de los empleados
                empleados_ids = request.data['empleados']

                # Obtener los objetos empleados correspondientes a esos IDs
                empleados = Empleado.objects.filter(id__in=empleados_ids)

                # Limpiar la relación actual y asociar los nuevos empleados
                proyecto.empleados.set(empleados)

            # Devuelve los datos actualizados del proyecto
            return Response(ProyectoSerializer(proyecto).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)