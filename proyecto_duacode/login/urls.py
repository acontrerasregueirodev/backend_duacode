from django.urls import path
from .views import login_view, logout_view, check_login  # Asegúrate de importar la vista personalizada

urlpatterns = [
    path('login/', login_view, name='login'),  # Ruta para el login
    path('logout/', logout_view, name='logout'),  # Ruta para el logout personalizada
    path('check_login/',check_login,name='check_login'),#Test para comprobar si está logueado
]