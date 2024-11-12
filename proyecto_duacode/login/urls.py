from django.urls import path
from .views import LoginView, LogoutView, CheckLoginView  # Importa las clases correctas

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),       # Utiliza .as_view() para las vistas basadas en clase
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check_login/', CheckLoginView.as_view(), name='check_login'),
]