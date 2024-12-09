import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.middleware.csrf import get_token
from sedes.models import Sede
from .models import Empleado, RolModel
from .serializers import EmpleadoSerializer, RolModelSerializer, OrganigramaSerializer, RolModelListSerializer
# from rest_framework.decorators import api_view
class WelcomeView(APIView):
    def get(self, request):
        # csrf_token = get_token(request)  # Obtén el token CSRF
        return Response({
            "message": "Bienvenido a Duacode TouchScreen!",
            # "csrfToken": csrf_token  # Incluye el token CSRF en la respuesta
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
        # Recuperar el objeto empleado desde la base de datos
        empleado = self.get_object()

        # Obtener los datos del request
        data = request.data

        # Asegurarse de deserializar el campo 'rol'
        try:
            rol_data = json.loads(data.get('rol', '{}'))  # Deserializar el JSON
            rol_id = rol_data.get('id')  # Acceder al campo 'id'
        except json.JSONDecodeError:
            return Response({"detail": "El campo 'rol' no es válido."}, status=400)

        # Asignar el valor de 'sede' como una instancia de Sede
        sede_id = data.get('sede')
        if sede_id:
            try:
                sede = Sede.objects.get(id=sede_id)  # Obtener la instancia de Sede
            except Sede.DoesNotExist:
                return Response({"detail": "La sede especificada no existe."}, status=400)
        else:
            return Response({"detail": "El campo 'sede' es obligatorio."}, status=400)
        # Actualizar el empleado con los nuevos datos
        empleado.nombre = data.get('nombre')
        empleado.apellido_1 = data.get('apellido_1')
        empleado.apellido_2 = data.get('apellido_2')
        empleado.email = data.get('email')
        empleado.telefono = data.get('telefono')
        empleado.rol_id = rol_id  # Actualizar el rol con el id deserializado
        empleado.sede = sede
        empleado.baja = data.get('baja') == 'true'
        empleado.excedencia = data.get('excedencia') == 'true'
        empleado.teletrabajo = data.get('teletrabajo') == 'true'
        empleado.vacaciones = data.get('vacaciones') == 'false'

        # Guardar el empleado actualizado
        empleado.save()

        return Response(EmpleadoSerializer(empleado).data)

        
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
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Genera la jerarquía completa del organigrama.
        """
        # Obtener el empleado raíz (sin supervisor)
        empleados_raiz = Empleado.objects.filter(supervisor__isnull=True)
        serializer = OrganigramaSerializer(empleados_raiz, many=True)
        return Response(serializer.data, status=200)
