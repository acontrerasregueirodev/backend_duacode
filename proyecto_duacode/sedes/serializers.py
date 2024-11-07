from rest_framework import serializers
from .models import Sede, SalaReuniones, ReservaSala
from core.models import Empleado  # Asegúrate de que el modelo Empleado está importado si lo usas

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'  # Incluye todos los campos del modelo Sede

class SalaReunionesSerializer(serializers.ModelSerializer):
    # Si deseas agregar un campo calculado (como is_ocupada), puedes hacerlo aquí.
    is_ocupada = serializers.BooleanField(read_only=True)  # campo calculado solo de lectura

    class Meta:
        model = SalaReuniones
        fields = '__all__'  # Incluye todos los campos del modelo SalaReuniones

class ReservaSalaSerializer(serializers.ModelSerializer):
    reservado_por = serializers.PrimaryKeyRelatedField(queryset=Empleado.objects.all())  # Relaciona con el modelo Empleado
    empleados_asistentes = serializers.PrimaryKeyRelatedField(queryset=Empleado.objects.all(), many=True, required=False)  # Relaciona con el modelo Empleado

    fecha_inicio = serializers.DateTimeField()  # Representa la fecha y hora de inicio como un campo DateTime
    fecha_fin = serializers.DateTimeField()  # Representa la fecha y hora de fin como un campo DateTime

    class Meta:
        model = ReservaSala
        fields = '__all__'  # Incluye todos los campos del modelo ReservaSala

    def validate(self, data):
        """
        Valida que las fechas de inicio y fin sean correctas.
        Asegúrate de que la fecha de inicio sea anterior a la fecha de fin.
        """
        if data['fecha_inicio'] >= data['fecha_fin']:
            raise serializers.ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")
        return data
