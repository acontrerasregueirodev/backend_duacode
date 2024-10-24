from django.db import models
from django.contrib.auth.models import User
from .qr_generator import generate_qr_code #Función para generar códigos QR
# Modelo para los roles
class RolModel(models.Model):
    ROL_CHOICES = [
        ('CEO', 'CEO'),
        ('CTO', 'CTO'),
        ('CFO', 'CFO'),
        ('LÍDER_DESARROLLO', 'Líder de Equipo de Desarrollo'),
        ('INGENIERO_FRONTEND', 'Ingeniero de Frontend'),
        ('INGENIERO_BACKEND', 'Ingeniero de Backend'),
        ('LÍDER_QA', 'Líder de QA'),
        ('INGENIERO_QA', 'Ingeniero de QA'),
        ('GERENTE_PROYECTO', 'Gerente de Proyecto'),
        ('COORDINADOR_PROYECTO', 'Coordinador de Proyecto'),
        ('GERENTE_PRODUCTO', 'Gerente de Producto'),
        ('PROPIETARIO_PRODUCTO', 'Propietario de Producto'),
        ('GERENTE_MARKETING', 'Gerente de Marketing'),
        ('ESPECIALISTA_MARKETING', 'Especialista en Marketing Digital'),
        ('GERENTE_VENTAS', 'Gerente de Ventas'),
        ('REPRESENTANTE_VENTAS', 'Representante de Ventas'),
        ('GERENTE_SOPORTE', 'Gerente de Soporte'),
        ('ESPECIALISTA_SOPORTE', 'Especialista en Soporte al Cliente'),
    ]

    nombre = models.CharField(max_length=50, choices=ROL_CHOICES)

    def __str__(self):
        return self.nombre



# Modelo para los empleados
class Empleado(models.Model):
    # Relación con el modelo User
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=50)  # Nombre
    apellido_1 = models.CharField(max_length=50)  # Primer Apellido
    apellido_2 = models.CharField(max_length=50)  # Segundo Apellido
    email = models.EmailField(unique=True)  # Correo electrónico, este campo será único
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Teléfono
    fecha_contratacion = models.DateField()  # Fecha de contratación
    cumpleaños = models.DateField()  # Fecha de nacimiento
    is_on_leave = models.BooleanField(default=False)  # Indicador de si está de baja/vacaciones
    foto = models.ImageField(upload_to='empleados/', blank=True, null=True)  # Foto del empleado
    
    # Relación con Rol
    rol = models.ForeignKey(RolModel, on_delete=models.CASCADE, default=5)
    # Relación con sede usando el nombre de la clase como cadena
    sede = models.ForeignKey('sedes.Sede', on_delete=models.CASCADE, null=True, blank=True)  # Relación con Sede

    # Campo para almacenar la imagen del código QR
    qr_code = models.ImageField(upload_to='codigo_qr/', blank=True, null=True)  # Cambia el path aquí

    def save(self, *args, **kwargs):
        # Generar y guardar el código QR utilizando la función modular
        qr_file = generate_qr_code(self)
        self.qr_code.save(f'{self.nombre}_{self.apellido_1}_qr.png', qr_file, save=False)

        # Llamar al método save() original para guardar el modelo
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellido_1} {self.apellido_2}'