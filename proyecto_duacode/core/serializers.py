from proyectos.models import Proyecto
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from .models import Empleado, RolModel



class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin']

class EmpleadoSerializer(serializers.ModelSerializer):
    proyectos = ProyectoSerializer(many=True, read_only=True)
    rol = serializers.PrimaryKeyRelatedField(queryset=RolModel.objects.all())
    #rol = RolModelSerializer()  # Cambiado a RolModelSerializer para incluir el nombre del rol
    #rol = serializers.CharField(source="rol.nombre", read_only=True)

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
    def validate_is_on_leave(self, value):
        # Convierte el valor 'false' a False y 'true' a True
        if isinstance(value, str):
            return value.lower() == 'true'
        return value
    def create(self, validated_data):
        empleado = Empleado.objects.create(**validated_data)
        return empleado
    
    def update(self, instance, validated_data):
        try:
            for attr, value in validated_data.items():
                if attr == 'foto' and isinstance(value, InMemoryUploadedFile):
                    instance.foto.save(value.name, value, save=False)
                else:
                    setattr(instance, attr, value)

            instance.save()  # Guarda la instancia
            return instance  # Retorna la instancia actualizada
        except Exception as e:
            print("Error al guardar el empleado:", e)
            raise
    


class RolModelSerializer(serializers.ModelSerializer):
    empleados = EmpleadoSerializer(many=True, read_only=True)  # Nested if detailed employee data is needed
    class Meta:
        model = RolModel
        fields = ['id', 'nombre','empleado']
        
class RolModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolModel
        fields = ['id', 'nombre']  # Solo los campos que quieres mostrar en la lista

