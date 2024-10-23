import logging
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import Empleado
from .serializers import EmpleadoSerializer

logger = logging.getLogger(__name__)
class EmpleadoViewset(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer


    def update(self, request, *args, **kwargs):
        # Obtiene la instancia del empleado que se va a actualizar
        partial = kwargs.pop('partial', False)  # Permite actualizaciones parciales
        instance = self.get_object()  # Obtiene el objeto actual

        # Log de datos recibidos
        print("Llego un update", request.data)

        # Crea un serializer con la instancia existente y los datos nuevos
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        # Valida el serializer
        if not serializer.is_valid():
            print("Errores de validación:", serializer.errors)  # Imprime errores de validación
            return Response(serializer.errors, status=400)  # Retorna errores de validación

        # Si es válido, guarda el objeto
        self.perform_update(serializer)

        # Retorna la respuesta con el objeto actualizado
        return Response(serializer.data)