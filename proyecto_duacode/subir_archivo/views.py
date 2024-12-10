from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny  # Permiso de autenticación
from rest_framework.response import Response
from rest_framework import status
from .forms import FileUploadForm
from .models import SubirArchivo

class UploadFile(APIView):
    permission_classes = [IsAuthenticated]  # Garantiza que el usuario esté autenticado

    def get_permissions(self):
        # Permite acceso sin autenticación solo para GET
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        files = SubirArchivo.objects.all()  # Obtener todos los archivos subidos
        file_list = [{"file_name": file.archivo.name, "uploaded_at": file.fecha_subida} for file in files]
        return Response(file_list)

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Guarda el archivo y la descripción
            return Response({'message': 'Archivo subido con éxito'}, status=status.HTTP_201_CREATED)
        return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)















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