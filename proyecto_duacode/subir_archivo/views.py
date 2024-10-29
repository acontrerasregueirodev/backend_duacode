from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import FileUploadForm
from .models import SubirArchivo
from core.views import BasePermisos  # Importa tu clase base de permisos

class Upload_File(BasePermisos, APIView):
    def get(self, request):
        # Renderiza el formulario y muestra los archivos subidos
        form = FileUploadForm()
        files = SubirArchivo.objects.all()  # Obtener todos los archivos subidos
        return render(request, 'file_upload/upload.html', {'form': form, 'files': files})

    def post(self, request):
        # Maneja la subida de archivos
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Guarda el archivo y la descripción
            return JsonResponse({'message': 'Archivo subido con éxito'})
        else:
            # Devuelve los errores del formulario si no es válido
            return JsonResponse({'error': form.errors}, status=400)















# from django.shortcuts import render, redirect
# from .forms import FileUploadForm
# from .models import SubirArchivo
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse

# def upload_file(request):
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()  # Guarda tanto el archivo como la descripción
#             return JsonResponse({'message': 'Archivo subido con éxito'})
#         else:
#             # Devuelve los errores del formulario si no es válido
#             return JsonResponse({'error': form.errors}, status=400)

#     else:
#         form = FileUploadForm()

#     files = SubirArchivo.objects.all()  # Obtener todos los archivos subidos
#     return render(request, 'file_upload/upload.html', {'form': form, 'files': files})