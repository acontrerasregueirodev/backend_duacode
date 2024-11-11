from rest_framework import serializers
from .models import ReservaSala, Sede, SalaReuniones
from core.models import Empleado  # Importar el modelo de Empleado
class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = ['id', 'nombre', 'direccion', 'ciudad', 'pais']
# Serializer para el modelo ReservaSala
class ReservaSalaSerializer(serializers.ModelSerializer):
    sala = serializers.PrimaryKeyRelatedField(queryset=SalaReuniones.objects.all())
    reservado_por = serializers.StringRelatedField()
    empleados_asistentes = serializers.PrimaryKeyRelatedField(queryset=Empleado.objects.all(), many=True)

    class Meta:
        model = ReservaSala
        fields = ['id', 'sala', 'reservado_por', 'fecha', 'hora_inicio', 'hora_fin', 'empleados_asistentes']
    
    def validate(self, data):
        if data['hora_inicio'] >= data['hora_fin']:
            raise serializers.ValidationError("La hora de inicio debe ser anterior a la hora de fin.")
        return data
    
