from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Empleado, RolModel
from .serializers import EmpleadoSerializer, EmpleadoUpdateSerializer
from rest_framework.viewsets import ModelViewSet


class BasePermisos(ModelViewSet):
    def get_permissions(self):
        # Requiere autenticación para crear, actualizar y eliminar
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        # Permitir acceso a cualquier usuario para listar o ver detalles
        return [AllowAny()]



def test_view():
    # Al conectarme a http://localhost:8000/api/empleados/test/ muestra una ruta 
    return HttpResponse("Esto es una prueba.")

class EmpleadoViewset(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()

    def get_permissions(self):
        # Require authentication for create, update, and delete actions
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]  # Requires authentication for these actions
        # Allow access to anyone for other actions like 'list' or 'retrieve'
        return [AllowAny()]

    def get_serializer_class(self):
        return EmpleadoSerializer

def update(self, request, *args, **kwargs):
    instance = self.get_object()  # Obtén la instancia actual del empleado
    data = request.data
    print("Datos de actualización recibidos: %s", data)

    # Actualiza manualmente los campos que deseas permitir
    campos_actualizables = [
        'nombre', 'apellido_1', 'apellido_2', 'email', 'telefono',
        'fecha_contratacion', 'cumpleaños', 'is_on_leave', 'rol', 'sede', 'foto'
    ]

    # Log de datos recibidos

    for campo in campos_actualizables:
        if campo in data:
            # En caso de que sea un archivo (foto), asegúrate de que sea un archivo válido
            if campo == 'foto' and 'foto' in request.FILES:
                setattr(instance, campo, request.FILES['foto'])
            else:
                setattr(instance, campo, data[campo])

    # Guarda la instancia actualizada
    instance.save()

    # Log de datos actualizados
    print("Datos de empleado actualizados: %s", instance)

    return Response({'mensaje': 'Empleado actualizado con éxito', 'empleado': instance.nombre}, status=status.HTTP_200_OK)


def create(self, request, *args, **kwargs):
    print("Datos de creación de empleado recibidos: %s", request.data)
    serializer = self.get_serializer(data=request.data)

    if serializer.is_valid():
        nombre = request.data.get('nombre')
        apellido_1 = request.data.get('apellido_1')
        username = f"{nombre.title()}.{apellido_1.title()}"
        password = 'password123'
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            logger.error("El nombre de usuario ya existe: %s", username)
            return Response({"error": "El nombre de usuario ya está en uso."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # Obtener el rol por ID o crear uno nuevo
        rol_data = request.data.get('rol')
        rol = None  # Inicializar rol

        if rol_data is not None:
            if isinstance(rol_data, int):  # Si rol_data es un ID
                rol = RolModel.objects.get(id=rol_data)  # Busca el rol por ID
            else:
                # Si es un objeto que contiene el nombre del rol
                rol, created = RolModel.objects.get_or_create(nombre=rol_data['nombre'])

        # Guardar el empleado con el usuario y el rol
        empleado = serializer.save(user=user, rol=rol)
        print("Empleado creado exitosamente: %s", serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("Errores de validación al crear empleado: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def destroy(self, request,pk=None):
    try:
        empleado = Empleado.objects.get(id=pk)
        empleado.delete()
        
        print("EMPLEADO ELIMINADO ID " ,pk)
        return Response({'message': 'Empleado eliminado con éxito.'}, status=status.HTTP_204_NO_CONTENT)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

