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
# Crear una instancia de Faker en español
fake = Faker('es_ES')

# Función para generar un número de teléfono español válido
def generar_telefono_espanol():
    prefijos_moviles = ['6', '7']  # Prefijos para móviles en España
    prefijos_fijos = ['91', '93', '95']  # Algunos prefijos fijos comunes
    if random.choice([True, False]):  # 50% de probabilidad de móvil o fijo
        numero = random.choice(prefijos_moviles) + ''.join([str(random.randint(0, 9)) for _ in range(8)])
    else:
        numero = random.choice(prefijos_fijos) + ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return numero

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

        # Función para descargar y guardar la foto
        def descargar_foto(nombre_usuario):
            foto_response = requests.get('https://randomuser.me/api/')
            foto_data = foto_response.json()
            foto_url = foto_data['results'][0]['picture']['large']
            foto_nombre = f"{nombre_usuario.lower().replace('.', '_')}.jpg"
            foto_path = os.path.join(settings.MEDIA_ROOT, 'empleados', foto_nombre)
            os.makedirs(os.path.dirname(foto_path), exist_ok=True)
            with open(foto_path, 'wb') as foto_file:
                foto_file.write(requests.get(foto_url).content)
            return f'empleados/{foto_nombre}'

        # Datos del CEO
        nombre_ceo = "Juan"
        apellido_1_ceo = "Pérez"
        email_ceo = "juan.perez@empresa.com"
        rol_ceo = created_roles['CEO']
        username_ceo = f"{nombre_ceo.capitalize()}.{apellido_1_ceo.capitalize()}"
        foto_ceo = descargar_foto(username_ceo)

        ceo_user = User.objects.create_user(username=username_ceo, password='password123', email=email_ceo)
        ceo = Empleado.objects.create(
            user=ceo_user,
            nombre=nombre_ceo,
            apellido_1=apellido_1_ceo,
            apellido_2= fake.last_name(),
            email=email_ceo,
            telefono=generar_telefono_espanol(),  # Teléfono español válido
            fecha_contratacion=date.today(),
            cumpleanos=date(1980, 5, 15),
            foto=foto_ceo,
            rol=rol_ceo,
            sede=None,
            baja=False,
            excedencia=False,
            teletrabajo=False,
            vacaciones=False,
            supervisor=None
        )
        print(f"CEO creado con username: {username_ceo} y foto: {foto_ceo}")

        # Datos del CTO
        nombre_cto = "Luis"
        apellido_1_cto = "Martínez"
        email_cto = "cto@company.com"
        rol_cto = created_roles['CTO']
        username_cto = f"{nombre_cto.capitalize()}.{apellido_1_cto.capitalize()}"
        foto_cto = descargar_foto(username_cto)

        cto_user = User.objects.create_user(username=username_cto, password='password123', email=email_cto)
        cto = Empleado.objects.create(
            user=cto_user,
            nombre=nombre_cto,
            apellido_1=apellido_1_cto,
            apellido_2=apellido_1_cto,
            email=email_cto,
            telefono=generar_telefono_espanol(),  # Teléfono español válido
            fecha_contratacion=date.today(),
            cumpleanos=date(1985, 8, 22),
            foto=foto_cto,
            rol=rol_cto,
            sede=None,
            baja=False,
            excedencia=False,
            teletrabajo=False,
            vacaciones=False,
            supervisor=ceo
        )
        print(f"CTO creado con username: {username_cto} y foto: {foto_cto}")

        # Datos del CFO
        nombre_cfo = "Ana"
        apellido_1_cfo = "López"
        email_cfo = "cfo@company.com"
        rol_cfo = created_roles['CFO']
        username_cfo = f"{nombre_cfo.capitalize()}.{apellido_1_cfo.capitalize()}"
        foto_cfo = descargar_foto(username_cfo)

        cfo_user = User.objects.create_user(username=username_cfo, password='password123', email=email_cfo)
        cfo = Empleado.objects.create(
            user=cfo_user,
            nombre=nombre_cfo,
            apellido_1=apellido_1_cfo,
            apellido_2=apellido_1_cfo,
            email=email_cfo,
            telefono=generar_telefono_espanol(),  # Teléfono español válido
            fecha_contratacion=date.today(),
            cumpleanos=date(1987, 11, 30),
            foto=foto_cfo,
            rol=rol_cfo,
            sede=None,
            baja=False,
            excedencia=False,
            teletrabajo=False,
            vacaciones=False,
            supervisor=ceo
        )
        print(f"CFO creado con username: {username_cfo} y foto: {foto_cfo}")

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
                foto_nombre = f"{nombre.lower()}.{apellido.lower()}.jpg"
                foto_path = os.path.join(settings.MEDIA_ROOT, 'empleados', foto_nombre)
                print(foto_path)
                
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
                    apellido_2=fake.last_name(),
                    email=email,
                    telefono=generar_telefono_espanol(),  # Teléfono español válido
                    fecha_contratacion=date.today(),
                    cumpleanos=cumpleanos[:10],  # Solo la fecha (yyyy-mm-dd)
                    foto=f'empleados/{foto_nombre}',  # Nombre de la foto descargada
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
            ('INGENIERO_FRONTEND', 2),
            ('INGENIERO_BACKEND', 2),
            ('INGENIERO_QA', 2),
            ('ESPECIALISTA_MARKETING', 2),
            ('ESPECIALISTA_SOPORTE', 2),
            ('COORDINADOR_PROYECTO', 2),
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
                foto_nombre = f'{nombre.lower()}.{apellido.lower()}.jpg'

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
                    apellido_2= fake.last_name(),
                    email=email,
                    telefono=generar_telefono_espanol(),  # Teléfono español válido
                    fecha_contratacion=date.today(),
                    cumpleanos=cumpleanos[:10],  # Solo la fecha (yyyy-mm-dd)
                    foto=f'empleados/{foto_nombre}',  # Ruta relativa a la foto
                    rol=random_rol,
                    sede=None,  # Aquí podrías asignar una sede si es necesario
                    baja=random.choice([True, False]),  # Valor aleatorio para baja
                    excedencia=random.choice([True, False]),  # Valor aleatorio para excedencia
                    teletrabajo=random.choice([True, False]),  # Valor aleatorio para teletrabajo
                    vacaciones=random.choice([True, False]),  # Valor aleatorio para vacaciones
                    supervisor=supervisor  # Asignamos el supervisor si tiene
                )

                empleados_creados += 1

                self.stdout.write(self.style.SUCCESS('Empleados y roles creados correctamente'))

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