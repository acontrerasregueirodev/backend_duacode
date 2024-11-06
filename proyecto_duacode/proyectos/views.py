# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Proyecto
from django.contrib.auth.decorators import login_required


def listar_proyectos(request):
    if request.method == 'GET':
        proyectos = Proyecto.objects.all()
        proyectos_data = [{"id": proyecto.id, "nombre": proyecto.nombre} for proyecto in proyectos]
        return JsonResponse(proyectos_data, safe=False, status=200)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'DELETE':
        proyecto.delete()
        return JsonResponse({'message': 'Proyecto eliminado exitosamente'}, status=200)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
