from django.db import models
from django.utils import timezone  # Para obtener la fecha/hora actual
from datetime import datetime  # Importar datetime para combinar fecha y hora

class Sede(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class SalaReuniones(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='salas')
    imagen_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.nombre} en {self.sede.nombre}'

    class Meta:
        db_table = 'salas_reuniones'

class ReservaSala(models.Model):
    sala = models.ForeignKey(SalaReuniones, on_delete=models.CASCADE, related_name='reservas')
    reservado_por = models.ForeignKey('core.Empleado', on_delete=models.CASCADE)
    fecha = models.DateField()  # Campo solo para la fecha
    hora_inicio = models.TimeField()  # Campo solo para la hora de inicio
    hora_fin = models.TimeField()  # Campo solo para la hora de fin
    empleados_asistentes = models.ManyToManyField('core.Empleado', related_name='reservas_asistentes', blank=True)
    motivo = models.CharField(max_length=200, null=True, blank=True)  # Campo para el motivo o título de la reserva

    def __str__(self):
        return f'Reserva de {self.sala.nombre} por {self.reservado_por} el {self.fecha}'

    class Meta:
        db_table = 'reservas_salas'
