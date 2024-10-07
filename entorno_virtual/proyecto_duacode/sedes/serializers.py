from rest_framework import serializers
from .models import Sede, SalaReuniones, ReservaSala

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = '__all__'


class SalaReunionesSerializer(serializers.ModelSerializer):
    sede = SedeSerializer(read_only=True)
    sede_id = serializers.PrimaryKeyRelatedField(
        queryset=Sede.objects.all(), source='sede', write_only=True
    )
    imagen_url = serializers.SerializerMethodField()  # Nuevo campo para la URL de la imagen

    class Meta:
        model = SalaReuniones
        fields = ['id', 'nombre', 'capacidad', 'sede', 'sede_id', 'imagen_url']  # Se incluye 'imagen_url'

    def get_imagen_url(self, obj):
        """
        Si la sala tiene una imagen, devuelve la URL completa de la imagen.
        Si no tiene, devuelve None.
        """
        request = self.context.get('request')
        if obj.imagen:
            return request.build_absolute_uri(obj.imagen.url)  # Construye la URL completa
        return None


class ReservaSalaSerializer(serializers.ModelSerializer):
    sala = SalaReunionesSerializer(read_only=True)
    sala_id = serializers.PrimaryKeyRelatedField(
        queryset=SalaReuniones.objects.all(), source='sala', write_only=True
    )

    class Meta:
        model = ReservaSala
        fields = ['id', 'sala', 'sala_id', 'fecha_inicio', 'fecha_fin', 'reservado_por']

