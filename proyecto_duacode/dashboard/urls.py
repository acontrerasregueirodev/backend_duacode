from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('protocolos/', views.protocolos, name='protocolos'),
]