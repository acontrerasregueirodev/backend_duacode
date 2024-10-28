import logging
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Empleado
from .serializers import EmpleadoSerializer, EmpleadoUpdateSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

logger = logging.getLogger(__name__)

def test_view(request):
    # Al conectarme a http://localhost:8000/api/empleados/test/ muestra una ruta 
    return HttpResponse("Esto es una prueba.")

class EmpleadoViewset(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()

    def get_permissions(self):
        # Solo requerir autenticación para la acción de creación
        if self.action == 'create':
            return [IsAuthenticated()]  # Requiere autenticación
        return [AllowAny()]  # Permitir acceso a cualquier usuario para otras acciones

    def get_serializer_class(self):
        # Utiliza el serializer adecuado basado en el método
        if self.request.method in ['PUT', 'PATCH']:
            return EmpleadoUpdateSerializer
        return EmpleadoSerializer

    def update(self, request, *args, **kwargs):
        # Obtiene la instancia del empleado que se va a actualizar
        partial = kwargs.pop('partial', False)  # Permite actualizaciones parciales
        instance = self.get_object()  # Obtiene el objeto actual

        # Log de datos recibidos
        logger.info("Datos de actualización recibidos: %s", request.data)

        # Usa EmpleadoUpdateSerializer para limitar los campos actualizables
        serializer = EmpleadoUpdateSerializer(instance, data=request.data, partial=partial)
        # Valida el serializer
        if not serializer.is_valid():
            logger.error("Errores de validación: %s", serializer.errors)
            return Response(serializer.errors, status=400)  # Retorna errores de validación
        # Si es válido, guarda el objeto
        self.perform_update(serializer)
        # Retorna la respuesta con el objeto actualizado
        return Response(serializer.data)

    def create(self, request):
        logger.info("Datos de creación de empleado recibidos: %s", request.data)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            nombre = request.data.get('nombre')
            apellido_1 = request.data.get('apellido_1')
            username = f"{nombre.lower()}.{apellido_1.lower()}"
            password = 'password123'
            email = request.data.get('email')

            if User.objects.filter(username=username).exists():
                logger.error("El nombre de usuario ya existe: %s", username)
                return Response({"error": "El nombre de usuario ya está en uso."}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            empleado = serializer.save(user=user)
            logger.info("Empleado creado exitosamente: %s", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Errores de validación al crear empleado: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

