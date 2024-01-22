from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('consulta_paciente/', views.consultaPaciente, name='consulta_paciente'),   
    path('paciente_resupesquisa/', views.pacienteResupesquisa, name='paciente_resupesquisa'),
]


