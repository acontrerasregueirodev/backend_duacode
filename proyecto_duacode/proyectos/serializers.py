# proyectos/serializers.py
from rest_framework import serializers
from .models import Proyecto
from core.models import Empleado  # Import the Empleado model from the empleados app
from core.serializers import EmpleadoSerializer  # Import the serializer if you want nested data

class ProyectoSerializer(serializers.ModelSerializer):
    
    empleados = EmpleadoSerializer(many=True)  # Indicar que es una relación Many-to-Many
    # Personalizar los campos de fechas
    fecha_inicio = serializers.DateField(format="%d-%m-%Y")  # Formatear la fecha
    fecha_fin = serializers.DateField(format="%d-%m-%Y")  # Formatear la fecha
    class Meta:
        model = Proyecto
        fields = '__all__'