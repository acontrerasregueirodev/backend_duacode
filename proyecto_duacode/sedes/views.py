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

    # def get_permissions(self):
    #     if self.action in ['create', 'update','delete']:
    #         print(IsAuthenticated())
    #         return [IsAuthenticated()]
    #     return [AllowAny()]

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



    def get_permissions(self):
        """Verifica que el usuario esté autenticado solo para actualizar o eliminar."""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]  # Solo autenticados pueden hacer update y delete
        return super().get_permissions()

    def perform_update(self, serializer):
        print("Intentando actualizar reserva con ID:", self.kwargs['pk'])
        
        # Obtener la reserva actual
        reserva = self.get_object()
        print(f"Reserva a actualizar: {reserva}")
        print(f"Usuario autenticado: {self.request.user.username}")

        # Permitir la actualización
        serializer.save()
        print(f"Reserva con ID {reserva.id} actualizada con éxito.")
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        print("Intentando eliminar reserva con ID:", kwargs['pk'])

        try:
            reserva = self.get_object()
            print(f"Usuario autenticado: {request.user.username}")

            # Eliminar la reserva sin restricciones
            reserva.delete()
            print(f"Reserva con ID {reserva.id} eliminada con éxito.")
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ReservaSala.DoesNotExist:
            print("Reserva no encontrada")
            raise NotFound(detail="Reserva no encontrada.")
