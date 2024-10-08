# contacto/urls.py
from django.urls import path
from .views import contacto_view

urlpatterns = [
    path('', contacto_view, name='contacto'),
]
