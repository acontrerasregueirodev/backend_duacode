from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .forms import FileUploadForm
from .models import SubirArchivo

class UploadFile(View):

    def get(self, request):
        # Renderiza el formulario y muestra los archivos subidos
        form = FileUploadForm()
        files = SubirArchivo.objects.all()  # Obtener todos los archivos subidos
        return render(request, 'file_upload/upload.html', {'form': form, 'files': files})

    def post(self, request):
        # Verificar si el usuario está autenticado para permitir la subida
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Debe estar autenticado para subir archivos'}, status=403)
        
        # Maneja la subida de archivos
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Guarda el archivo y la descripción
            return JsonResponse({'message': 'Archivo subido con éxito'})
        else:
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