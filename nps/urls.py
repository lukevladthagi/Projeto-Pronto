from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('clinica/', views.npsClinica, name='npsClinica'),
    path('emergencia/', views.npsEmergencia, name='npsEmergencia'),
    path('posalta/', views.npsPosAlta, name='npsPosAlta'),
    path('listagem/<int:id_esc>', views.listagem, name='listagem'),
    path('formularios/', views.formularios, name='formularios'),
    path('dashboardnps/', views.dashboardnps, name='dashboardnps'),
    path('prontoplayer/', views.prontoPlayer, name='prontoPlayer'),

]


