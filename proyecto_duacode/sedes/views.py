from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Sede, SalaReuniones, ReservaSala
from .serializers import SedeSerializer, SalaReunionesSerializer, ReservaSalaSerializer

class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()
    serializer_class = SedeSerializer

    def get_permissions(self):
        """
        Devuelve los permisos basados en la acción que se esté realizando.
        """
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]  # Para otras acciones como 'list', cualquier usuario puede acceder


class SalaReunionesViewSet(viewsets.ModelViewSet):
    queryset = SalaReuniones.objects.all()
    serializer_class = SalaReunionesSerializer

    def get_permissions(self):
        """
        Devuelve los permisos basados en la acción que se esté realizando.
        """
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]  # Para otras acciones como 'list', cualquier usuario puede acceder

    def get_queryset(self):
        queryset = super().get_queryset()
        sede_id = self.request.query_params.get('sede_id')
        if sede_id:
            queryset = queryset.filter(sede_id=sede_id)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Sobrescribe el método list para incluir las imágenes de las salas.
        """
        queryset = self.get_queryset()
        serializer = SalaReunionesSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

class ReservaSalaViewSet(viewsets.ModelViewSet):
    queryset = ReservaSala.objects.all()
    serializer_class = ReservaSalaSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        sala_id = self.request.query_params.get('sala_id')
        if sala_id:
            queryset = queryset.filter(sala_id=sala_id)
        
        ahora = timezone.now().time()
        hoy = timezone.now().date()

        if self.request.query_params.get('pasadas') == 'true':
            queryset = queryset.filter(fecha__lt=hoy)

        if self.request.query_params.get('futuras') == 'true':
            queryset = queryset.filter(fecha__gt=hoy)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sala = serializer.validated_data['sala']
        fecha = serializer.validated_data['fecha']
        hora_inicio = serializer.validated_data['hora_inicio']
        hora_fin = serializer.validated_data['hora_fin']

        reservas_existentes = ReservaSala.objects.filter(
            sala=sala,
            fecha=fecha,
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio
        )

        if reservas_existentes.exists():
            return Response(
                {'detail': 'La sala ya está reservada en este intervalo de tiempo.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def eliminar_reserva(self, request, pk=None):
        """
        Acción personalizada para eliminar una reserva específica.
        """
        reserva = get_object_or_404(ReservaSala, pk=pk)
        reserva.delete()
        return Response({'message': 'Reserva eliminada exitosamente'}, status=status.HTTP_200_OK)