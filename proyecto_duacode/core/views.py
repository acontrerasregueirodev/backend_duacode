from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Empleado
from .serializers import EmpleadoSerializer
from rest_framework.response import Response 
from rest_framework.views import APIView
from django.middleware.csrf import get_token




class WelcomeView(APIView):
    def get(self, request):
        csrf_token = get_token(request) # Obtén el token CSRF
        return Response({            
            "message": "Bienvenido a Duacode TouchScreen!",
            "csrfToken": csrf_token  # Incluye el token CSRF en la respuesta
        })

class EmpleadoViewset(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

    def get_permissions(self):
        if self.action in ['create', 'update','partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def create(self, request, *args, **kwargs):
        print("Datos de creación de empleado recibidos:", request.data)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtiene la instancia actual del empleado
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            print("Datos validados para guardar:", serializer.validated_data)  # Registro de datos validados
            serializer.save()  # Guarda los cambios en la base de datos
            return Response({'mensaje': 'Empleado actualizado con éxito', 'empleado': serializer.data}, status=status.HTTP_200_OK)
        else:
            print("Errores de validación:", serializer.errors)  # Registro de errores de validación
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        print("stamos en destro empleados")
        try:
            empleado = Empleado.objects.get(id=pk)
            empleado.delete()
            return Response({'message': 'Empleado eliminado con éxito.'}, status=status.HTTP_204_NO_CONTENT)
        except Empleado.DoesNotExist:
            return Response({'error': 'Empleado no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

