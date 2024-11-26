from django.db import models
from django.contrib.auth.models import User
from .qr_generator import generate_qr_code  # Función para generar códigos QR
from datetime import date

# Modelo para los roles
from django.db import models

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
    
    nombre = models.CharField(max_length=255)
    # Definir la relación ManyToMany para supervisar a otros roles
    supervisa_a = models.ManyToManyField(
        'self', 
        symmetrical=False,  # No es simétrica, o sea, si A supervisa a B, B no supervisa a A
        related_name='supervisado_por',  # Nombre para referirse a los roles supervisados
        blank=True  # Esta relación es opcional
    )

    def __str__(self):
        return dict(self.ROL_CHOICES).get(self.nombre, self.nombre)

    def get_supervisados(self):
        """
        Devuelve todos los roles que este rol supervisa.
        """
        return self.supervisa_a.all()

    def get_supervisores(self):
        """
        Devuelve todos los roles que supervisan a este rol.
        """
        return self.supervisado_por.all()

    def clean(self):
        # Evitar que un rol se supervise a sí mismo
        if self in self.supervisa_a.all():
            raise ValidationError('Un rol no puede supervisarse a sí mismo.')


# Modelo para los empleados
class Empleado(models.Model):
    # Relación con el modelo User
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=50)  # Nombre
    apellido_1 = models.CharField(max_length=50)  # Primer Apellido
    apellido_2 = models.CharField(max_length=50)  # Segundo Apellido
    email = models.EmailField(unique=True)  # Correo electrónico
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Teléfono
    fecha_contratacion = models.DateField()  # Fecha de contratación
    cumpleanos = models.DateField()  # Fecha de nacimiento
    foto = models.ImageField(upload_to='empleados/', blank=True, null=True)  # Foto
    rol = models.ForeignKey(RolModel, on_delete=models.CASCADE)  # Relación con Rol
    sede = models.ForeignKey('sedes.Sede', on_delete=models.CASCADE, null=True, blank=True)  # Relación con Sede

    # Campos booleanos para la situación del empleado
    baja = models.BooleanField(default=False)  # Si está de baja
    excedencia = models.BooleanField(default=False)  # Si está en excedencia
    teletrabajo = models.BooleanField(default=False)  # Si está teletrabajando
    vacaciones = models.BooleanField(default=False)  # Si está de vacaciones
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)  # Agregar relación de supervisor con otro empleado
    # Campo para almacenar la imagen del código QR
    qr_code = models.ImageField(upload_to='codigo_qr/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generar y guardar el código QR
        if not self.pk:
            qr_file = generate_qr_code(self)
            self.qr_code.save(f'{self.nombre}_{self.apellido_1}_qr.png', qr_file, save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellido_1} {self.apellido_2}'

    def get_supervisor(self):
        """
        Devuelve el supervisor directo del empleado basándose en el rol.
        """
        supervisores = self.rol.get_supervisores()
        return supervisores.first() if supervisores.exists() else None

    def tiempo_en_empresa(self):
        """
        Calcula el tiempo que lleva el empleado en la empresa (en años y meses).
        """
        today = date.today()
        delta = today - self.fecha_contratacion
        years = delta.days // 365
        months = (delta.days % 365) // 30
        return f'{years} años y {months} meses'

    def obtener_informacion_completa(self):
        """
        Obtiene toda la información relevante del empleado.
        """
        return {
            'nombre_completo': f'{self.nombre} {self.apellido_1} {self.apellido_2}',
            'cumpleanos': self.cumpleanos,
            'tiempo_en_empresa': self.tiempo_en_empresa(),
            'foto': self.foto.url if self.foto else None,
            'correo': self.email,
            'telefono': self.telefono,
            'sede': self.sede.nombre if self.sede else 'No asignada',
            'supervisor': self.get_supervisor().nombre if self.get_supervisor() else 'No tiene supervisor',
            'puesto': self.rol.nombre,
            'vacaciones': 'Sí' if self.vacaciones else 'No',
            'baja': 'Sí' if self.baja else 'No',
            'excedencia': 'Sí' if self.excedencia else 'No',
            'teletrabajo': 'Sí' if self.teletrabajo else 'No',
        }
        
        