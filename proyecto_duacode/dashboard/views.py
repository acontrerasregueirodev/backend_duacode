from django.shortcuts import render
from django.core.paginator import Paginator
from collections import defaultdict
from datetime import timedelta
from django.utils.timezone import now
from core.models import Empleado
from sedes.models import ReservaSala, Sede
from proyectos.models import Proyecto  
from subir_archivo.models import SubirArchivo

def dashboard(request):
    # Obtener todos los empleados
    empleados = Empleado.objects.all().order_by('id')

    # Configurar la paginación
    paginator = Paginator(empleados, 10)  # 10 empleados por página
    page_number = request.GET.get('page')  # Obtener el número de la página desde la URL
    page_obj = paginator.get_page(page_number)

    # Contar proyectos por empleado (relación Many-to-Many)
    proyectos_por_empleado = {}
    for empleado in page_obj:  # Iteramos solo sobre los empleados de la página actual
        proyectos_por_empleado[empleado.id] = empleado.proyectos.count()  # Usamos el related_name 'proyectos'

    # Contar reuniones a las que asistió cada empleado
    reuniones_asistidas_por_empleado = {}
    for empleado in page_obj:
        # Contar cuántas reuniones ha reservado este empleado
        reuniones_reservadas = ReservaSala.objects.filter(reservado_por=empleado).count()

        # Contar cuántas reuniones tiene este empleado en 'empleados_asistentes'
        reuniones_asistidas = ReservaSala.objects.filter(empleados_asistentes=empleado).count()

        # Sumar ambas
        reuniones_asistidas_por_empleado[empleado.id] = reuniones_reservadas + reuniones_asistidas
    
    # Obtener el total de empleados por proyecto
    proyectos_empleados = {}
    proyectos = Proyecto.objects.all()
    for proyecto in proyectos:
        proyectos_empleados[proyecto.nombre] = proyecto.empleados.count()

    # Contar empleados por rol
    empleados_por_rol = defaultdict(int)
    for empleado in page_obj:
        empleados_por_rol[empleado.rol.nombre] += 1

    # Contar empleados por sede
    empleados_por_sede = defaultdict(int)
    for empleado in page_obj:
        if empleado.sede:
            empleados_por_sede[empleado.sede.nombre] += 1

    # Resto del código para obtener reuniones por sede y otras variables
    hoy = now().date()
    fecha_fin = hoy + timedelta(days=5)

    reuniones_por_sede = {}
    sedes = Sede.objects.all()
    for sede in sedes:
        reuniones = (
            ReservaSala.objects.filter(
                sala__sede=sede,
                fecha__range=(hoy, fecha_fin)
            )
            .order_by('fecha')
        )
        reuniones_dias = {str(hoy + timedelta(days=i)): 0 for i in range(6)}
        for reunion in reuniones:
            reuniones_dias[str(reunion.fecha)] += 1
        reuniones_por_sede[sede.nombre] = reuniones_dias

    # Pasar los proyectos de cada empleado como un diccionario
    proyectos_lista = [
        {
            'empleado_id': empleado.id,
            'proyectos_count': proyectos_por_empleado.get(empleado.id, 0),
            'reuniones_asistidas': reuniones_asistidas_por_empleado.get(empleado.id, 0),
            'supervisor': f'{empleado.supervisor.nombre} {empleado.supervisor.apellido_1} {empleado.supervisor.apellido_2}' if empleado.supervisor else 'No tiene supervisor'  # Agregar supervisor
        }
        for empleado in page_obj  # Solo empleados de la página actual
    ]

    # Pasar los empleados paginados al contexto
    context = {
        'empleados': empleados,
        'reuniones_por_sede': reuniones_por_sede,
        'proyectos_lista': proyectos_lista,  # Los proyectos contados para cada empleado
        'dias': [str(hoy + timedelta(days=i)) for i in range(6)],
        'page_obj': page_obj,  # Para la paginación
        'proyectos_empleados': proyectos_empleados,  # Total de empleados por proyecto
        'empleados_por_rol': dict(empleados_por_rol),  # Contar empleados por rol
        'empleados_por_sede': dict(empleados_por_sede),  # Contar empleados por sede
    }

    return render(
        request,
        'dashboard.html',  # Ruta del template
        context,
    )


def proyectos(request):
    proyectos = Proyecto.objects.all()  # Consulta todos los proyectos
    context = {'proyectos': proyectos}  # Contexto para la plantilla
    return render(request, 'proyectos/proyectos.html', context)

def protocolos(request):
    # Obtener todos los empleados
    protocolos = SubirArchivo.objects.all()
    print(protocolos)
    context = {'protocolos': protocolos}
    return render(request, 'protocolos/protocolos.html', context)
    
    # def get(self, request):
    #     files = SubirArchivo.objects.all()  # Obtener todos los archivos subidos
    #     file_list = [{
    #         "titulo": file.titulo,            # Título del archivo
    #         "file_name": file.file.name,     # Nombre del archivo
    #         "descripcion": file.descripcion, # Descripción del archivo
    #         "uploaded_at": file.uploaded_at  # Fecha de subida
    #     } for file in files]
    #     return Response(file_list)