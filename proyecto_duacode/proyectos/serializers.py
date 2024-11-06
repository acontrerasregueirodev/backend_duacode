# proyectos/serializers.py

from rest_framework import serializers
from .models import Proyecto

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'  # Esto incluirá todos los campos del modelo Proyecto
