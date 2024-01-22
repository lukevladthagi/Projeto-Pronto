from django.contrib import admin
from django.urls import path, include
from notificar import views

urlpatterns = [
    path('', views.form_1, name='form_1'),
    path('formulario/', views.form_2, name='telaIni'),
    path('form_finalizado/', views.form_3, name='form_3'),
    path('relatorio_notificar/', views.relatorio_notificar, name='relatorio_notificar'),
    path('planoAcao/', views.planoAcao, name='planoAcao'),
    path('cadastroPt1/', views.cadastro_Pt1, name='cadastroPt1'),
    path('cadastro/<int:tp_cad>', views.cadastro, name='cadastro'),

]


