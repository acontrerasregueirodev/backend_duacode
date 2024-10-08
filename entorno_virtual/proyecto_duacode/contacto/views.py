# contacto/views.py
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactoForm

def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']
            
            # Dirección de correo a la que se enviará el mensaje
            destinatario = 'adrian.contreras.rookie@gmail.com'  # Cambia esto a la dirección deseada
            
            # Enviar el correo
            send_mail(
                f'Mensaje de {nombre}',  # Asunto
                mensaje,  # Contenido del mensaje
                email,  # Correo del remitente
                [destinatario],  # Lista de destinatarios
            )
            return render(request, 'contacto/exito.html')  # Redirigir a una página de éxito
    else:
        form = ContactoForm()
    
    return render(request, 'contacto/contacto.html', {'form': form})
