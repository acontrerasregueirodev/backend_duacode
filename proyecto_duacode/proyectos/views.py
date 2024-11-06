
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Proyecto
from .serializers import ProyectoSerializer

class ProyectoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo de Proyecto, que permite realizar operaciones CRUD.
    """
    queryset = Proyecto.objects.all()  # Define el queryset que se utilizará para recuperar los proyectos
    serializer_class = ProyectoSerializer  # Define el serializador para el modelo Proyecto
    permission_classes = [AllowAny]  # Permite el acceso a cualquier usuario (sin autenticación ni permisos específicos)

    # Esto configura que todas las operaciones CRUD sean aceptadas:
    # - LIST (GET): Listar todos los proyectos
    # - CREATE (POST): Crear un nuevo proyecto
    # - RETRIEVE (GET): Ver los detalles de un proyecto específico
    # - UPDATE (PUT/PATCH): Actualizar un proyecto existente
    # - DESTROY (DELETE): Eliminar un proyecto