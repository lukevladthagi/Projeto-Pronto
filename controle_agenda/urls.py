from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('controle_consulta/', views.controle_consulta, name='controle_consulta'),
    path('controle_exame/', views.controle_exame, name='controle_exame'),
    path('api/events/', views.get_events, name='get_events'),
    path('selecionaView/', views.selecionaView, name='selecionaView'),
    path('selecionaData/', views.selecionaData, name='selecionaData'),
]
