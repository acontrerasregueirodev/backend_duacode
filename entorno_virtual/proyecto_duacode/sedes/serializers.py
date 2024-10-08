from rest_framework import serializers
from .models import Sede, SalaReuniones, ReservaSala
from core.models import Empleado  # Asegúrate de tener la importación correcta de 'Empleado'


class SedeSerializer(serializers.ModelSerializer):
    # Incluir las salas de reuniones relacionadas con la sede
    salas = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Sede
        fields = ['id', 'nombre', 'direccion', 'ciudad', 'pais', 'salas']


class SalaReunionesSerializer(serializers.ModelSerializer):
    # Mostrar los detalles de la sede relacionada
    sede = SedeSerializer(read_only=True)
    # Incluir las reservas de la sala
    reservas = serializers.StringRelatedField(many=True, read_only=True)
    # Mostrar si la sala está ocupada usando la propiedad 'is_ocupada'
    is_ocupada = serializers.ReadOnlyField()

    class Meta:
        model = SalaReuniones
        fields = ['id', 'nombre', 'capacidad', 'sede', 'imagen_url', 'reservas', 'is_ocupada']


class ReservaSalaSerializer(serializers.ModelSerializer):
    # Mostrar los detalles de la sala reservada
    sala = SalaReunionesSerializer(read_only=True)
    # Mostrar el nombre del empleado que reservó la sala
    reservado_por = serializers.StringRelatedField(read_only=True)
    # Mostrar los asistentes a la reunión
    empleados_asistentes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = ReservaSala
        fields = ['id', 'sala', 'reservado_por', 'fecha_inicio', 'fecha_fin', 'empleados_asistentes']
