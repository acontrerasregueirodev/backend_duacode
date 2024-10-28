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
    proyectos = ProyectoSerializer(many=True, read_only=True)  # Relación opcional, solo lectura
    rol = RolModelSerializer()  # Usar el serializer anidado para el campo rol

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
        # Extraer los datos del rol
        rol_data = validated_data.pop('rol', None)

        # Crear el empleado
        empleado = Empleado.objects.create(**validated_data)

        # Si hay datos de rol, crea o asocia el rol
        if rol_data:
            rol, created = RolModel.objects.get_or_create(**rol_data)
            empleado.rol = rol
            empleado.save()

        return empleado

class EmpleadoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido_1', 'apellido_2', 'email', 'telefono']
