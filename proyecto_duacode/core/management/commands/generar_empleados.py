import os
import random
import requests
from django.core.management.base import BaseCommand
from faker import Faker
from core.models import Empleado, RolModel
from proyectos.models import Proyecto
from sedes.models import Sede, SalaReuniones, ReservaSala
from django.conf import settings
from django.contrib.auth.models import User
from datetime import time, date, timedelta, datetime
from django.utils import timezone


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

        # Crear roles con jerarquía
        rol_nombres = [
            'CEO', 'CTO', 'CFO', 'LÍDER_DESARROLLO', 'INGENIERO_FRONTEND', 'INGENIERO_BACKEND', 
            'LÍDER_QA', 'INGENIERO_QA', 'GERENTE_PROYECTO', 'COORDINADOR_PROYECTO', 'GERENTE_PRODUCTO',
            'PROPIETARIO_PRODUCTO', 'GERENTE_MARKETING', 'ESPECIALISTA_MARKETING', 'GERENTE_VENTAS', 
            'REPRESENTANTE_VENTAS', 'GERENTE_SOPORTE', 'ESPECIALISTA_SOPORTE'
        ]

        roles = {}
        for nombre in rol_nombres:
            rol, created = RolModel.objects.get_or_create(nombre=nombre)
            roles[nombre] = rol

        # Definir la jerarquía de supervisores
        jerarquia = {
            'CEO': None,
            'CTO': 'CEO',
            'LÍDER_DESARROLLO': 'CTO',
            'INGENIERO_FRONTEND': 'LÍDER_DESARROLLO',
            'INGENIERO_BACKEND': 'LÍDER_DESARROLLO',
            'LÍDER_QA': 'CTO',
            'INGENIERO_QA': 'LÍDER_QA',
            'GERENTE_PROYECTO': 'CTO',
            'COORDINADOR_PROYECTO': 'GERENTE_PROYECTO',
            'CFO': 'CEO',
            'GERENTE_PRODUCTO': 'CFO',
            'PROPIETARIO_PRODUCTO': 'GERENTE_PRODUCTO',
            'GERENTE_MARKETING': 'CFO',
            'ESPECIALISTA_MARKETING': 'GERENTE_MARKETING',
            'GERENTE_VENTAS': 'CFO',
            'REPRESENTANTE_VENTAS': 'GERENTE_VENTAS',
            'GERENTE_SOPORTE': 'CFO',
            'ESPECIALISTA_SOPORTE': 'GERENTE_SOPORTE'
        }

        # Crear roles jerárquicos
        created_roles = {}
        for nombre, supervisor in jerarquia.items():
            # Asegurar que todos los supervisores existen antes de asignar un rol
            if supervisor and supervisor not in created_roles:
                supervisor_rol = RolModel.objects.create(nombre=supervisor)
                created_roles[supervisor] = supervisor_rol

            # Crear el rol si no existe
            rol, created = RolModel.objects.get_or_create(nombre=nombre)
            created_roles[nombre] = rol

        # Crear un solo CEO, CTO y CFO
        ceo_user = User.objects.create_user(username="ceo", password='password123', email="ceo@company.com")
        ceo = Empleado.objects.create(
            user=ceo_user,
            nombre="Juan",
            apellido_1="Pérez",
            apellido_2="Gómez",
            email="juan.perez@empresa.com",
            telefono="123456789",  # Número de teléfono
            fecha_contratacion=date.today(),
            cumpleanos=date(1980, 5, 15),
            foto=None,
            rol=created_roles['CEO'],
            sede=None,
            baja=False,
            excedencia=False,
            teletrabajo=False,
            vacaciones=False,
            supervisor=None
        )

        cto_user = User.objects.create_user(username="cto", password='password123', email="cto@company.com")
        cto = Empleado.objects.create(
            user=cto_user,
            nombre="Luis",
            apellido_1="Martínez",
            apellido_2="Gómez",
            email="cto@company.com",
            telefono="987654321",  # Número de teléfono
            fecha_contratacion=date.today(),
            cumpleanos=date(1985, 8, 22),
            foto=None,
            rol=created_roles['CTO'],
            sede=None,
            baja=False,
            excedencia=False,
            teletrabajo=False,
            vacaciones=False,
            supervisor=ceo
        )

        cfo_user = User.objects.create_user(username="cfo", password='password123', email="cfo@company.com")
        cfo = Empleado.objects.create(
            user=cfo_user,
            nombre="Ana",
            apellido_1="López",
            apellido_2="Fernández",
            email="cfo@company.com",
            telefono="912345678",  # Número de teléfono
            fecha_contratacion=date.today(),
            cumpleanos=date(1987, 11, 30),
            foto=None,
            rol=created_roles['CFO'],
            sede=None,
            baja=False,
            excedencia=False,
            teletrabajo=False,
            vacaciones=False,
            supervisor=ceo
        )

        # Crear los empleados del escalón medio
        empleados_por_crear_jerarquia = [
            ('LÍDER_DESARROLLO', 3),
            ('LÍDER_QA', 2),
            ('GERENTE_PROYECTO', 2),
            ('GERENTE_PRODUCTO', 1),
            ('PROPIETARIO_PRODUCTO', 1),
            ('GERENTE_MARKETING', 2),
            ('ESPECIALISTA_MARKETING', 2),
            ('GERENTE_VENTAS', 2),
            ('REPRESENTANTE_VENTAS', 2),
            ('GERENTE_SOPORTE', 3),
            ('ESPECIALISTA_SOPORTE', 2),
        ]

        empleados_creados = 0
        for rol_nombre, cantidad in empleados_por_crear_jerarquia:
            random_rol = created_roles[rol_nombre]
            for _ in range(cantidad):
                # Generar un usuario aleatorio con randomuser.me
                response = requests.get('https://randomuser.me/api/')
                data = response.json()
                user_info = data['results'][0]
                nombre = user_info['name']['first']
                apellido = user_info['name']['last']
                email = user_info['email']
                telefono = user_info['phone']
                cumpleanos = user_info['dob']['date']
                foto_url = user_info['picture']['large']
                
                # Descargar la foto
                foto_response = requests.get(foto_url)
                foto_nombre = f"{random_rol.nombre.lower().replace(' ', '_')}_foto_{empleados_creados + 1}.jpg"
                foto_path = os.path.join(settings.MEDIA_ROOT, 'empleados', foto_nombre)
                
                with open(foto_path, 'wb') as f:
                    f.write(foto_response.content)

                # Asignar el supervisor de acuerdo a la jerarquía
                supervisor_rol = jerarquia.get(random_rol.nombre)
                if supervisor_rol:
                    # Filtrar los empleados que ya tienen el rol de supervisor y que no están de baja ni tienen excedencia
                    posibles_supervisores = Empleado.objects.filter(rol=created_roles[supervisor_rol], baja=False, excedencia=False)
                    # Elegir uno aleatoriamente
                    supervisor = posibles_supervisores.order_by('?').first() if posibles_supervisores.exists() else None
                else:
                    supervisor = None  # Si no tiene supervisor, asignamos None

                # Para los Ingenieros de Backend y Frontend, asignar un Líder de Desarrollo aleatorio
                if random_rol.nombre in ['INGENIERO_FRONTEND', 'INGENIERO_BACKEND']:
                    lider_desarrollo = Empleado.objects.filter(rol=created_roles['LÍDER_DESARROLLO']).order_by('?').first()
                    supervisor = lider_desarrollo

                # Crear el empleado
                user = User.objects.create_user(username=email.split('@')[0], password='password123', email=email)
                empleado = Empleado.objects.create(
                    user=user,
                    nombre=nombre,
                    apellido_1=apellido,
                    apellido_2=apellido,
                    email=email,
                    telefono=telefono,
                    fecha_contratacion=date.today(),
                    cumpleanos=cumpleanos[:10],  # Solo la fecha (yyyy-mm-dd)
                    foto=foto_nombre,  # Nombre de la foto descargada
                    rol=random_rol,
                    sede=None,
                    baja=False,
                    excedencia=False,
                    teletrabajo=False,
                    vacaciones=False,
                    supervisor=supervisor  # Asignamos el supervisor
                )

                empleados_creados += 1

        # Crear los empleados del escalón más bajo (ya añadido)
        empleados_por_crear_bajo = [
            ('INGENIERO_FRONTEND', 10),
            ('INGENIERO_BACKEND', 10),
            ('INGENIERO_QA', 5),
            ('ESPECIALISTA_MARKETING', 5),
            ('ESPECIALISTA_SOPORTE', 5),
            ('COORDINADOR_PROYECTO', 5),
            ('PROPIETARIO_PRODUCTO', 2),
        ]

        for rol_nombre, cantidad in empleados_por_crear_bajo:
            random_rol = created_roles[rol_nombre]
            for _ in range(cantidad):
                # Generar un usuario aleatorio con randomuser.me
                response = requests.get('https://randomuser.me/api/')
                data = response.json()
                user_info = data['results'][0]
                nombre = user_info['name']['first']
                apellido = user_info['name']['last']
                email = user_info['email']
                telefono = user_info['phone']
                cumpleanos = user_info['dob']['date']
                foto_url = user_info['picture']['large']
                
                # Descargar la foto
                foto_response = requests.get(foto_url)
                foto_nombre = f"{random_rol.nombre.lower().replace(' ', '_')}_foto_{empleados_creados + 1}.jpg"
                foto_path = os.path.join(settings.MEDIA_ROOT, 'empleados', foto_nombre)
                
                with open(foto_path, 'wb') as f:
                    f.write(foto_response.content)

                # Asignar el supervisor de acuerdo a la jerarquía
                supervisor_rol = jerarquia.get(random_rol.nombre)
                # Asignar el supervisor de acuerdo a la jerarquía de manera aleatoria
                if supervisor_rol:
                    # Filtrar los empleados que ya tienen el rol de supervisor y que no están de baja ni tienen excedencia
                    posibles_supervisores = Empleado.objects.filter(rol=created_roles[supervisor_rol], baja=False, excedencia=False)
                    # Elegir uno aleatoriamente
                    supervisor = posibles_supervisores.order_by('?').first() if posibles_supervisores.exists() else None
                else:
                    supervisor = None  # Si no tiene supervisor, asignamos None

                # Crear el usuario
                user = User.objects.create_user(username=email.split('@')[0], password='password123', email=email)
                
                # Crear el empleado
                empleado = Empleado.objects.create(
                    user=user,
                    nombre=nombre,
                    apellido_1=apellido,
                    apellido_2=apellido,
                    email=email,
                    telefono=telefono,
                    fecha_contratacion=date.today(),
                    cumpleanos=cumpleanos[:10],  # Solo la fecha (yyyy-mm-dd)
                    foto=foto_nombre,  # Nombre de la foto descargada
                    rol=random_rol,
                    sede=None,  # Aquí podrías asignar una sede si es necesario
                    baja=False,
                    excedencia=False,
                    teletrabajo=False,
                    vacaciones=False,
                    supervisor=supervisor  # Asignamos el supervisor si tiene
                )

                empleados_creados += 1

                self.stdout.write(self.style.SUCCESS(
                    f'Empleado creado: {empleado.nombre} {empleado.apellido_1} {empleado.apellido_2} | '
                    f'Rol: {empleado.rol.nombre} | Supervisor: {empleado.supervisor.nombre if empleado.supervisor else "Ninguno"}'
                ))
        # Generar sedes
        sedes = ['Sede Principal', 'Sede Secundaria', 'Sede Internacional']
        for nombre_sede in sedes:
            sede = Sede.objects.create(nombre=nombre_sede, direccion=f"Calle {nombre_sede}")
            sedes_objs.append(sede)

        self.stdout.write(self.style.SUCCESS('Sedes generadas correctamente.'))



        # Generar proyectos
        for i in range(1, 6):
            proyecto = Proyecto.objects.create(
                nombre=f'Proyecto {i}',
                descripcion=f'Descripción del proyecto {i}',
                fecha_inicio=date.today(),
                fecha_fin=date.today() + timedelta(days=30)
            )
            proyectos.append(proyecto)

        self.stdout.write(self.style.SUCCESS('Proyectos generados correctamente.'))


        # Generar salas de reuniones y asignarles imágenes
        nombres_salas = ['Sala 1', 'Sala 2', 'Sala 3']

        for sede in sedes_objs:
            for nombre_sala in nombres_salas:
                imagen_aleatoria = random.choice(imagenes)
                imagen_url = f"{settings.MEDIA_URL}salas_reuniones/{imagen_aleatoria}"

                sala = SalaReuniones.objects.create(
                    nombre=nombre_sala,
                    capacidad=random.randint(5, 20),
                    sede=sede,
                    imagen_url=imagen_url
                )
                salas_objs.append(sala)

        self.stdout.write(self.style.SUCCESS(f'Se han generado {len(salas_objs)} salas de reuniones con imágenes.'))

                # Generar 200 reservas de salas en los próximos 15 días, de 1 hora cada una
        for _ in range(200):
            sala_aleatoria = random.choice(salas_objs)
            fecha_reserva = timezone.now().date() + timedelta(days=random.randint(1, 15))
            hora_inicio = time(random.randint(8, 17), 0)
            hora_fin = (datetime.combine(datetime.today(), hora_inicio) + timedelta(hours=1)).time()

            asistentes = random.sample(list(Empleado.objects.all()), random.randint(2, 5))
            empleado_reservador = random.choice(Empleado.objects.all())

            reserva = ReservaSala.objects.create(
                sala=sala_aleatoria,
                fecha=fecha_reserva,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                reservado_por=empleado_reservador
            )
            reserva.empleados_asistentes.set(asistentes)
            reserva.save()

        self.stdout.write(self.style.SUCCESS('Se han generado las 200 reservas de las salas de reuniones correctamente.'))