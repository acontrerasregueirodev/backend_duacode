from rest_framework import serializers
from .models import Sede, SalaReuniones, ReservaSala
from core.models import Empleado


# Serializer para los empleados
class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['id', 'nombre', 'apellido_1', 'apellido_2', 'email']


# Serializer para las salas de reuniones
class SalaReunionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaReuniones
        fields = ['id', 'nombre', 'capacidad', 'sede', 'imagen_url']


# Serializer para las sedes, incluyendo sus salas de reuniones
class SedeSerializer(serializers.ModelSerializer):
    salas = SalaReunionesSerializer(many=True, read_only=True)

    class Meta:
        model = Sede
        fields = ['id', 'nombre', 'direccion', 'ciudad', 'pais', 'salas']


# Serializer para las reservas de sala
class ReservaSalaSerializer(serializers.ModelSerializer):
    sala = SalaReunionesSerializer(read_only=True)
    reservado_por = EmpleadoSerializer(read_only=True)
    empleados_asistentes = EmpleadoSerializer(many=True, read_only=True)

    class Meta:
        model = ReservaSala
        fields = ['id', 'sala', 'reservado_por', 'fecha', 'hora_inicio', 'hora_fin', 'empleados_asistentes']

    def create(self, validated_data):
        asistentes_data = self.initial_data.get('empleados_asistentes', [])
        reserva = ReservaSala.objects.create(**validated_data)
        if asistentes_data:
            asistentes = Empleado.objects.filter(id__in=asistentes_data)
            reserva.empleados_asistentes.set(asistentes)
        return reserva

