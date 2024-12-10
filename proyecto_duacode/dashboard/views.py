# views.py
from proyectos.models import Proyecto
from core.models import Empleado
from django.shortcuts import render
from django.utils.timezone import now, timedelta
from sedes.models import Sede, ReservaSala

def dashboard(request):
    empleados = Empleado.objects.all()

    # Contar proyectos por empleado (relación Many-to-Many)
    proyectos_por_empleado = {}
    for empleado in empleados:
        proyectos_por_empleado[empleado.id] = Proyecto.objects.filter(empleados=empleado).count()

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

    return render(
        request,
        'dashboard.html',
        {
            'empleados': empleados,
            'reuniones_por_sede': reuniones_por_sede,
            'proyectos_por_empleado': proyectos_por_empleado,
            'dias': [str(hoy + timedelta(days=i)) for i in range(6)],
        },
    )
