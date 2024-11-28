from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Empleado, RolModel
from rest_framework.decorators import action
from .serializers import EmpleadoSerializer, RolModelSerializer, OrganigramaSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from rest_framework.viewsets import ReadOnlyModelViewSet

class WelcomeView(APIView):
    def get(self, request):
        csrf_token = get_token(request)  # Obtén el token CSRF
        return Response({
            "message": "Bienvenido a Duacode TouchScreen!",
            "csrfToken": csrf_token  # Incluye el token CSRF en la respuesta
        })

class RolViewSet(ReadOnlyModelViewSet):
    """
    ViewSet para listar y recuperar roles.
    """
    queryset = RolModel.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RolModelListSerializer  # Usar RolModelListSerializer para /api/roles/
        return RolModelSerializer  # Usar RolModelSerializer para otros casos

class EmpleadoViewset(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtiene la instancia actual del empleado
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  # Guarda los cambios en la base de datos
            return Response({'mensaje': 'Empleado actualizado con éxito', 'empleado': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            empleado = Empleado.objects.get(id=pk)
            empleado.delete()
            return Response({'message': 'Empleado eliminado con éxito.'}, status=status.HTTP_204_NO_CONTENT)
        except Empleado.DoesNotExist:
            return Response({'error': 'Empleado no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='perfil')
    def perfil(self, request):
        """
        Esta acción personalizada permite que un empleado vea su perfil.
        """
        empleado = self.queryset.filter(user=request.user).first()  # Cambiado 'usuario' a 'user'
        if empleado:
            serializer = self.get_serializer(empleado)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Empleado no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class OrganigramaView(APIView):
    def get(self, request):
        """
        Genera la jerarquía del organigrama, incluyendo solo parentId para todos los empleados.
        """
        empleados = Empleado.objects.all()

        # Función para construir la jerarquía solo con parentId
        def build_hierarchy(empleado):
            # Crear el diccionario de un empleado
            emp_data = {
                'id': empleado.id,
                'nombre': empleado.nombre,
                'apellido_1': empleado.apellido_1,
                'puesto': empleado.rol.nombre if empleado.rol else 'Sin Rol',
                'foto': empleado.foto.url if empleado.foto else None,
                'parentId': empleado.supervisor.id if empleado.supervisor else None
            }
            return emp_data

        # Construir la jerarquía, solo con parentId para todos los empleados
        organigrama_data = [build_hierarchy(empleado) for empleado in empleados]

        return Response(organigrama_data, status=200)