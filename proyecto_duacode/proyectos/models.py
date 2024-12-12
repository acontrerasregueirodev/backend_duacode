from django.db import models

# Create your models here.
from django.db import models
from core.models import Empleado  # Importa el modelo Empleado desde la app empleados

class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del proyecto
    descripcion = models.TextField()  # Descripción del proyecto
    fecha_inicio = models.DateField()  # Fecha de inicio del proyecto
    fecha_fin = models.DateField(blank=True, null=True)  # Fecha de finalización
    empleados = models.ManyToManyField(Empleado, related_name='proyectos')  # Relación ManyToMany con Empleado
    fotos = models.ImageField(upload_to='proyectos/', blank=True, null=True)  # Campo para subir fotos
    director = models.ForeignKey(Empleado, related_name='proyectos_dirigidos', blank=True, null=True, on_delete=models.SET_NULL)  # Relación con un director del proyecto
    fecha_entrega = models.DateField(blank=True, null=True)  # Fecha de entrega (puede ser nula)

    def __str__(self):
        return self.nombre