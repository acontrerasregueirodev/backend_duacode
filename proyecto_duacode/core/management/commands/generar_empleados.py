import os
from django.utils import timezone
from datetime import timedelta
import random
import requests
import qrcode  # Importar la biblioteca para generar códigos QR
from django.core.management.base import BaseCommand
from faker import Faker
from core.models import Empleado, RolModel
from proyectos.models import Proyecto
from sedes.models import Sede, SalaReuniones, ReservaSala
from django.conf import settings
from django.contrib.auth.models import User  # Importa el modelo User

class Command(BaseCommand):
    help = 'Genera datos ficticios para empleados, proyectos, sedes, salas y reuniones'

    def handle(self, *args, **kwargs):
        fake = Faker()
        empleados = []
        proyectos = []
        sedes_objs = []
        salas_objs = []

        # Path to the folder with room images
        imagenes_path = os.path.join(settings.MEDIA_ROOT, 'salas_reuniones')
        imagenes = [f for f in os.listdir(imagenes_path) if f.endswith('.jpg')]

        # Definir roles y verificar si ya existen
        rol_nombres = [
            'CEO', 'CTO', 'CFO', 'Líder de Equipo de Desarrollo',
            'Ingeniero de Frontend', 'Ingeniero de Backend', 'Líder de QA',
            'Ingeniero de QA', 'Gerente de Proyecto', 'Coordinador de Proyecto',
            'Gerente de Producto', 'Propietario de Producto', 'Gerente de Marketing',
            'Especialista en Marketing Digital', 'Gerente de Ventas', 
            'Representante de Ventas', 'Gerente de Soporte', 
            'Especialista en Soporte al Cliente'
        ]

        roles = []
        for nombre in rol_nombres:
            rol, created = RolModel.objects.get_or_create(nombre=nombre)
            roles.append(rol)

        self.stdout.write(self.style.SUCCESS(f'Se han generado {len(roles)} roles.'))

        # Generar sedes
        sedes = ['Sede Principal', 'Sede Secundaria', 'Sede Internacional']

        for nombre_sede in sedes:
            sede = Sede.objects.create(
                nombre=nombre_sede,
                direccion=f'Calle {random.randint(1, 100)}',
                ciudad='Ciudad ' + nombre_sede,
                pais='País ' + nombre_sede
            )
            sedes_objs.append(sede)

        self.stdout.write(self.style.SUCCESS(f'Se han generado {len(sedes_objs)} sedes.'))

        # Generar empleados
        for _ in range(5):
            response = requests.get('https://randomuser.me/api/')
            data = response.json()

            gender = data['results'][0]['gender']
            if gender == 'male':
                nombre = fake.first_name_male()
            else:
                nombre = fake.first_name_female()

            photo_url = data['results'][0]['picture']['medium']
            photo_response = requests.get(photo_url)

            apellido_1 = fake.last_name()
            apellido_2 = fake.last_name()
            photo_filename = f'{nombre}_{apellido_1}_{apellido_2}.jpg'
            photo_path = os.path.join(settings.MEDIA_ROOT, 'empleados', photo_filename)

            with open(photo_path, 'wb') as f:
                f.write(photo_response.content)

            # Crear un usuario para el empleado
            username = f"{nombre}.{apellido_1}"
            user = User.objects.create_user(username=username, email=fake.unique.email(), password='password123')

            rol_aleatorio = random.choice(roles)
            sede_aleatoria = random.choice(sedes_objs)

            empleado = Empleado(
                user=user,  # Asigna el usuario creado
                nombre=nombre,
                apellido_1=apellido_1,
                apellido_2=apellido_2,
                email=user.email,  # Usar el email del usuario
                telefono=fake.phone_number(),
                fecha_contratacion=fake.date_between(start_date='-5y', end_date='today'),
                cumpleaños=fake.date_of_birth(minimum_age=18, maximum_age=65),
                is_on_leave=fake.boolean(chance_of_getting_true=20),
                foto=f'empleados/{photo_filename}',
                rol=rol_aleatorio,
                sede=sede_aleatoria
            )
            empleado.save()
        self.stdout.write(self.style.SUCCESS(f'Empleado creado: {nombre} {apellido_1} {apellido_2}'))

        self.stdout.write(self.style.SUCCESS(f'Se han generado {Empleado.objects.count()} empleados.'))

        # Generar proyectos
        for _ in range(10):
            proyecto = Proyecto(
                nombre=fake.company(),
                descripcion=fake.paragraph(),
                fecha_inicio=fake.date_between(start_date='-2y', end_date='today'),
                fecha_fin=fake.date_between(start_date='today', end_date='+1y') if random.choice([True, False]) else None
            )
            proyectos.append(proyecto)

        Proyecto.objects.bulk_create(proyectos)
        self.stdout.write(self.style.SUCCESS(f'Se han generado {len(proyectos)} proyectos.'))

        # Asignar empleados a proyectos
        for proyecto in proyectos:
            num_empleados = random.randint(1, 10)
            proyecto.empleados.set(random.sample(list(Empleado.objects.all()), num_empleados))

        self.stdout.write(self.style.SUCCESS('Se han asignado empleados a los proyectos.'))

        # Generar salas de reuniones y asignarles imágenes
        nombres_salas = ['Sala 1', 'Sala 2', 'Sala 3']

        for sede in sedes_objs:
            for nombre_sala in nombres_salas:
                # Asignar una imagen aleatoria de la carpeta y crear la URL
                imagen_aleatoria = random.choice(imagenes)
                imagen_url = f"{settings.MEDIA_URL}salas_reuniones/{imagen_aleatoria}"

                sala = SalaReuniones.objects.create(
                    nombre=nombre_sala,
                    capacidad=random.randint(5, 20),
                    sede=sede,
                    imagen_url=imagen_url  # Asignar la URL completa
                )
                salas_objs.append(sala)

        self.stdout.write(self.style.SUCCESS(f'Se han generado {len(salas_objs)} salas de reuniones con imágenes.'))

        # Generar reservas de salas
        for _ in range(10):
            sala_aleatoria = random.choice(salas_objs)
            fecha_inicio = timezone.now() + timedelta(days=random.randint(1, 30), hours=random.randint(8, 18))
            fecha_fin = fecha_inicio + timedelta(hours=2)

            asistentes = random.sample(list(Empleado.objects.all()), random.randint(2, 5))
            empleado_reservador = random.choice(Empleado.objects.all())

            reserva = ReservaSala.objects.create(
                sala=sala_aleatoria,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                reservado_por=empleado_reservador
            )
            reserva.empleados_asistentes.set(asistentes)
            reserva.save()

        self.stdout.write(self.style.SUCCESS('Se han generado las reservas de las salas de reuniones correctamente.'))
