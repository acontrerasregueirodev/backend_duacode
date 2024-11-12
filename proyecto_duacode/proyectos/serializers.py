# proyectos/serializers.py
from rest_framework import serializers
from .models import Proyecto
from core.models import Empleado  # Import the Empleado model from the empleados app
from core.serializers import EmpleadoSerializer  # Import the serializer if you want nested data

class ProyectoSerializer(serializers.ModelSerializer):
    empleados = EmpleadoSerializer(many=True, read_only=True)  # Nested if detailed employee data is needed
    
    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'empleados']
