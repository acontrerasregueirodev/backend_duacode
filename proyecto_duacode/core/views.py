import logging
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Empleado
from .serializers import EmpleadoSerializer, EmpleadoUpdateSerializer
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)


@login_required
def test_view(request):
    #Al conectarme a http://localhost:8000/api/empleados/test/ muestra una ruta 
    return HttpResponse("Esto es una prueba.")
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


