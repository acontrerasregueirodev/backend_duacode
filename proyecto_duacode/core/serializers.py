from rest_framework import serializers
from .models import Empleado, RolModel

class RolModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolModel
        fields = ['id', 'nombre']

class EmpleadoSerializer(serializers.ModelSerializer):
    # Incluir el serializer del rol
    rol = RolModelSerializer()
    # Para incluir el supervisor, que se obtiene a través del modelo Empleado
    supervisor = serializers.SerializerMethodField()

    class Meta:
        model = Empleado
        fields = [
            'id', 'nombre', 'apellido_1', 'apellido_2', 'email', 'telefono', 'fecha_contratacion',
            'cumpleanos', 'foto', 'rol', 'sede', 'baja', 'excedencia', 'teletrabajo', 'vacaciones', 'qr_code',
            'supervisor'
        ]
    
    def get_supervisor(self, obj):
        """
        Devuelve la información del supervisor (nombre) del empleado.
        """
        if obj.supervisor:  # Si el empleado tiene un supervisor
            supervisor = obj.supervisor
            return f'{supervisor.nombre} {supervisor.apellido_1} {supervisor.apellido_2}'
        return 'No tiene supervisor'


# Serializer con formato para React_OrgChart
class OrganigramaSerializer(serializers.ModelSerializer):
    # Campo recursivo para los empleados supervisados
    children = serializers.SerializerMethodField() # Campo personalizado obtenido de get_children
    rol = RolModelSerializer()

    class Meta:
        model = Empleado
        fields = ['id', 'nombre', 'apellido_1', 'apellido_2', 'rol', 'children', 'foto']

    def get_children(self, obj):
        """
        Devuelve una lista de empleados supervisados por este empleado en el formato esperado.
        """
        supervisados = Empleado.objects.filter(supervisor=obj)
        return OrganigramaSerializer(supervisados, many=True).data