import logging
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Empleado
from .serializers import EmpleadoSerializer, EmpleadoUpdateSerializer

logger = logging.getLogger(__name__)

class EmpleadoViewset(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    
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

# Nueva vista para el panel de empleados, protegida por IsAuthenticated
class PanelEmpleadosView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # Solo permite acceso a usuarios autenticados
    
    def list(self, request):
        empleados = Empleado.objects.all()  # Lógica para obtener los empleados
        serializer = EmpleadoSerializer(empleados, many=True)  # Serializa los datos
        return Response(serializer.data)  # Retorna los empleados
