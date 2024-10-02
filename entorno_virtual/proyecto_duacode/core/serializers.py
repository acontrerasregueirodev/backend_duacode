# core/serializers.py
from rest_framework import serializers
from .models import Empleado
from rest_framework import serializers
from proyectos.models import Proyecto 
class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'

#Creamos un serializador que nos permita convertir Empleado a JSON y viceversa
# Serializador para el modelo Empleado que incluye los proyectos asociados
class Serializador_Empleado(serializers.ModelSerializer):
    proyectos = ProyectoSerializer(many=True)  # Incluir los proyectos del empleado

    class Meta:
        model = Empleado
        fields = '__all__'  # Incluye todos los campos del modelo Empleado
