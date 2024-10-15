import os
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect,render
from django.conf import settings
#from django.shortcuts import render
from .models import CodigoQR

import qrcode



# codigo_qr/views.py

# Vista para escanear códigos QR
def scan(request):
    return render(request, 'codigo_qr/qr_reader.html')  # Asegúrate de tener la plantilla correcta


def generar_qr(request):
    img_path = None
    if request.method == 'POST':
        data = request.POST.get('data')
        nombre = request.POST.get('nombre')

        if data and nombre:
            # Generar el código QR
            qr = qrcode.QRCode(version=2, box_size=10, border=2)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="blue", back_color="white")

            # Definir la ruta de la imagen generada
            img_dir = os.path.join(settings.MEDIA_ROOT, 'codigo_qr', f'{nombre}.png')

            # Asegurarse de que el directorio exista
            os.makedirs(os.path.dirname(img_dir), exist_ok=True)

            # Guardar la imagen en un archivo
            img.save(img_dir)

            # Guardar en la base de datos
            CodigoQR.objects.create(nombre=nombre, qr_image=f'codigo_qr/{nombre}.png')
            img_path = f'codigo_qr/{nombre}.png'
            return redirect('generar_qr')  # Redirigir después de guardar

    return render(request, 'codigo_qr/generar_qr.html', {'img_path': img_path})