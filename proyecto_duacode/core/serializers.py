from rest_framework import serializers
from .models import Empleado, RolModel
from proyectos.models import Proyecto

class RolModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolModel
        fields = ['id', 'nombre']

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin']

class EmpleadoSerializer(serializers.ModelSerializer):
    proyectos = ProyectoSerializer(many=True, read_only=True)  # Optional, read-only relation
    rol = serializers.PrimaryKeyRelatedField(queryset=RolModel.objects.all()) #

    class Meta:
        model = Empleado
        fields = [
            'id',
            'nombre',
            'apellido_1',
            'apellido_2',
            'email',
            'telefono',
            'fecha_contratacion',
            'cumpleaños',
            'is_on_leave',
            'foto',
            'proyectos',
            'rol',
            'sede',
        ]

    def create(self, validated_data):
        empleado = Empleado.objects.create(**validated_data)
        return empleado

class EmpleadoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido_1', 'apellido_2', 'email', 'telefono']
