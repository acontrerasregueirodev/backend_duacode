from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import ReservaSala, Sede
from core.models import Empleado
from .serializers import ReservaSalaSerializer, SedeSerializer
from rest_framework.exceptions import NotFound

class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()  # Recuperar todas las sedes
    serializer_class = SedeSerializer  # Usar el serializer definido antes

class ReservaSalaViewSet(viewsets.ModelViewSet):
    queryset = ReservaSala.objects.all()
    serializer_class = ReservaSalaSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        fecha = self.request.query_params.get('fecha', None)
        if fecha:
            queryset = queryset.filter(fecha=fecha)
        return queryset

    def perform_create(self, serializer):
        try:
            empleado = Empleado.objects.get(user=self.request.user)  # Si tienes esta relación
            serializer.save(reservado_por=empleado)
        except Empleado.DoesNotExist:
            raise ValueError("No se encontró un Empleado asociado al usuario actual.")

    def destroy(self, request, *args, **kwargs):
        """Método para eliminar una reserva"""
        print("Intentando eliminar reserva con ID:", kwargs['pk'])  # Imprime el ID de la reserva a eliminar

        try:
            # Obtener la reserva por ID
            reserva = self.get_object()  # Esto busca la reserva según el `pk` pasado en la URL
            
            # Imprimir detalles de la reserva
            print(f"reserva :{reserva}")
            print(f"Reserva encontrada: {reserva.id} - {reserva.reservado_por.user.username}")
            print(f"Usuario autenticado: {request.user.username}")

            # Verificar si el usuario tiene permiso para eliminar esta reserva
            if reserva.reservado_por.user != request.user:
                print(f"Usuario {request.user.username} no tiene permisos para eliminar esta reserva.")
                return Response(
                    {"detail": "No tienes permiso para eliminar esta reserva."},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            reserva.delete()  # Eliminar la reserva
            print(f"Reserva con ID {reserva.id} eliminada con éxito.")  # Confirmación de eliminación
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReservaSala.DoesNotExist:
            print("Reserva no encontrada")  # Mensaje si no se encuentra la reserva
            raise NotFound(detail="Reserva no encontrada.")