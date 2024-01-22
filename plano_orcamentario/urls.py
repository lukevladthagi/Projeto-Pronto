from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #path('ficha_identidade/', views.fichaIdentidade, name='ficha_identidade'),
    path('abertura_orcamento/', views.abertura_orcamento, name='abertura_orcamento'),
    path('controle_orcamento/', views.controle_orcamento, name='controle_orcamento'),
    path('dashboard_orcamento/', views.dashboard_orcamento, name='dashboard_orcamento'),
    path('fechamento_orcamento/', views.fechamento_orcamento, name='fechamento_orcamento'),
]


