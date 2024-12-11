from rest_framework import serializers
from .models import Empleado, RolModel
import json
from sedes.serializers import SedeSerializer
from sedes.models import Sede
# from proyectos.serializers import ProyectoSerializer
class RolModelListSerializer(serializers.ModelSerializer):
    rol_display = serializers.SerializerMethodField()
    class Meta:
        model = RolModel
        fields = ['id', 'nombre','rol_display']  
        # Asegúrate de incluir los campos que quieres mostrar
    def get_rol_display(self,obj):
        # Mapea los códigos a sus nombres legibles
        rol_map = dict(RolModel.ROL_CHOICES)
        return rol_map.get(obj.nombre, obj.nombre)  # Devuelve el nombre legible o el valor en caso de no encontrarlo
class RolModelSerializer(serializers.ModelSerializer):
    rol_display = serializers.SerializerMethodField()
    class Meta:
        model = RolModel
        fields = ['id', 'nombre','rol_display']

    def get_rol_display(self,obj):
        # Mapea los códigos a sus nombres legibles
        rol_map = dict(RolModel.ROL_CHOICES)
        return rol_map.get(obj.nombre, obj.nombre)  # Devuelve el nombre legible o el valor en caso de no encontrarlo
        
class EmpleadoSerializer(serializers.ModelSerializer):
    foto = serializers.CharField(required=False)  # Aceptar una URL en lugar de un archivo
    qr_code = serializers.CharField(required=False)  # Aceptar una URL en lugar de un archivo
    # Incluir el serializer del rol
    rol = serializers.PrimaryKeyRelatedField(queryset=RolModel.objects.all())
    sede = serializers.PrimaryKeyRelatedField(queryset=Sede.objects.all())
    # rol = RolModelSerializer()    
    rol_display = serializers.CharField(source='rol.rol_display', read_only=True)  # Añadir el nombre legible del rol
    # sede = SedeSerializer()
    # proyecto = ProyectoSerializer()
    # Para incluir el supervisor, que se obtiene a través del modelo Empleado
    supervisor = serializers.SerializerMethodField()
    # Personalizar los campos de fechas
    fecha_contratacion = serializers.DateField(format="%d-%m-%Y")  # Formatear la fecha
    cumpleanos = serializers.DateField(format="%d-%m-%Y")  # Formatear la fecha
    class Meta:
        model = Empleado
        fields = [
            'id', 'nombre', 'apellido_1', 'apellido_2', 'email', 'telefono', 'fecha_contratacion',
            'cumpleanos', 'foto', 'rol','rol_display', 'sede', 'baja', 'excedencia', 'teletrabajo', 'vacaciones', 'qr_code',
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
    


    def update(self, instance, validated_data):
        try:
            # Extraemos los datos relacionados con 'rol' y 'supervisor' de validated_data
            rol_data = validated_data.pop('rol', None)
            supervisor_data = validated_data.pop('supervisor', None)

            # Si 'rol' es una cadena (JSON como string), la deserializamos
            if rol_data and isinstance(rol_data, str):
                try:
                    rol_data = json.loads(rol_data)
                    print("Rol deserializado correctamente.")
                except json.JSONDecodeError as e:
                    print(f"Error al deserializar el rol: {e}")
                    raise ValueError("Error al deserializar el rol")

            # Si hay datos de rol, actualizamos el rol
            if rol_data:
                rol_instance = instance.rol
                for attr, value in rol_data.items():
                    setattr(rol_instance, attr, value)
                rol_instance.save()
                print(f"Rol actualizado: {rol_instance}")

            # Si se pasó un supervisor, actualizamos
            if supervisor_data:
                instance.supervisor = supervisor_data
                print(f"Supervisor actualizado: {supervisor_data}")

            # Actualizamos el resto de los campos del empleado
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                print(f"Campo {attr} actualizado con valor {value}")

            # Guardamos los cambios
            instance.save()
            print(f"Empleado {instance.nombre} actualizado correctamente.")
            return instance

        except Exception as e:
            # En caso de error, lo mostramos en consola
            print(f"Error al actualizar el empleado: {e}")
            raise e  # Volvemos a lanzar la excepción para que Django maneje el error



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
        # Realiza una consulta a la base de datos para obtener todos los empleados que tienen como supervisor al empleado actual (obj).
        supervisados = Empleado.objects.filter(supervisor=obj)
        return OrganigramaSerializer(supervisados, many=True).data