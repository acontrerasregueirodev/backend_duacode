from rest_framework import viewsets, status
from .models import Sede, SalaReuniones, ReservaSala
from .serializers import SedeSerializer, SalaReunionesSerializer, ReservaSalaSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.views import BasePermisos
class SedeViewSet(BasePermisos):


    queryset = Sede.objects.all()
    serializer_class = SedeSerializer


class SalaReunionesViewSet(BasePermisos):
    queryset = SalaReuniones.objects.all()
    serializer_class = SalaReunionesSerializer

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


class ReservaSalaViewSet(BasePermisos):
    queryset = ReservaSala.objects.all()
    serializer_class = ReservaSalaSerializer


    def get_queryset(self):
        queryset = super().get_queryset()
        sala_id = self.request.query_params.get('sala_id')
        if sala_id:
            queryset = queryset.filter(sala_id=sala_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sala = serializer.validated_data['sala']
        fecha_inicio = serializer.validated_data['fecha_inicio']
        fecha_fin = serializer.validated_data['fecha_fin']

        # Comprobar disponibilidad
        reservas_existentes = ReservaSala.objects.filter(
            sala=sala,
            fecha_inicio__lt=fecha_fin,
            fecha_fin__gt=fecha_inicio
        )
        if reservas_existentes.exists():
            return Response(
                {'detail': 'La sala ya está reservada en este intervalo de tiempo.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

