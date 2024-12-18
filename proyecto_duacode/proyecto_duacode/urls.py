"""
URL configuration for proyecto_duacode project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import WelcomeView  # Asegúrate de importar tu vista

#from core.views import PanelEmpleadosView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # Rutas para empleados
    # path('api/', include('core.urls')),      # Rutas para roles
    path('api/proyectos/', include('proyectos.urls')),  # Rutas de proyectos
    path('upload/', include('subir_archivo.urls')),  # Asegúrate de que la ruta sea correcta
    path('api/sedes/',include('sedes.urls')),
    path('mapa/',include('mapa.urls')),
    path('contacto/', include('contacto.urls')),    
    path('codigo_qr/', include('codigo_qr.urls')),
    path('auth/', include('login.urls')),  # Include login app URLs
    path('', WelcomeView.as_view(), name='welcome'),  # Ruta raíz del proyecto
    path('dashboard/', include('dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Solo en desarrollo, para servir archivos estáticos y multimedia
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

    

# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
