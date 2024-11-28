from rest_framework import serializers
from .models import ReservaSala, Sede, SalaReuniones
from core.models import Empleado  # Importar el modelo de Empleado

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['id', 'nombre', 'apellido_1', 'apellido_2', 'email']

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = ['id', 'nombre', 'direccion', 'ciudad', 'pais']

# Serializer para las salas de reuniones
class SalaReunionesSerializer(serializers.ModelSerializer):
    reservas = serializers.SerializerMethodField()  # Para incluir las reservas asociadas a la sala
    sede = SedeSerializer() #Mostrar todos los datos de la sede
    class Meta:
        model = SalaReuniones
        fields = ['id', 'nombre', 'capacidad', 'sede', 'imagen_url', 'reservas']

    def get_reservas(self, obj):
        """
        Devuelve las reservas asociadas a esta sala.
        """
        # Accede a todas las reservas asociadas con la sala
        reservas = ReservaSala.objects.filter(sala=obj)
        # Serializa las reservas
        return ReservaSalaSerializer(reservas, many=True).data

# Serializer para el modelo ReservaSala
class ReservaSalaSerializer(serializers.ModelSerializer):
    sala = serializers.PrimaryKeyRelatedField(queryset=SalaReuniones.objects.all())
    reservado_por = serializers.StringRelatedField()
    empleados_asistentes = serializers.SerializerMethodField()  # SerializerMethodField para empleados_asistentes
    motivo = serializers.CharField(max_length=200, required=False, allow_blank=True)  # Añadir el campo motivo

    class Meta:
        model = ReservaSala
        fields = ['id', 'sala', 'reservado_por', 'fecha', 'hora_inicio', 'hora_fin', 'empleados_asistentes', 'motivo']

    def validate(self, data):
        # Validar que la hora de inicio sea anterior a la hora de fin
        if data['hora_inicio'] >= data['hora_fin']:
            raise serializers.ValidationError("La hora de inicio debe ser anterior a la hora de fin.")
        return data

    def get_empleados_asistentes(self, obj):
        """
        Devuelve los datos de los empleados asistentes a la reunión.
        """
        # Accede al campo `empleados_asistentes` de la instancia (obj)
        empleados = obj.empleados_asistentes.all()  # Suponiendo que sea una relación ManyToMany
        # Serializa los datos de los empleados asistentes
        return EmpleadoSerializer(empleados, many=True).data
