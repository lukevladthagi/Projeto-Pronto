from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('prerelatorio2_1/<int:id_set>', views.preRelatoriov2_1, name='preRelatoriov2_1'),
    path('prerelatoriov2/', views.preRelatoriov2, name='preRelatoriov2'),
    path('relatorio/<str:setor>/<str:data>', views.relatorio, name='relatorio'),
    path('relatoriov2/<str:setor>/<str:data>', views.relatoriov2, name='relatoriov2'),
    path('relatoriov3/<str:setor>/<str:data>', views.relatoriov3, name='relatoriov3'),
    path('filtroParaDashboard', views.dashboardProctor, name='dashboardProctor'),
    path('avaliacao/', views.avaliacao, name='avaliacao'),
    path('escolheSetor/', views.escolheSetor, name='escolheSetor'),
    path('iniciar_avaliacao/<int:id_dim>/<int:id_set>', views.iniciarAval, name='iniciar_avaliacao'),
    path('indicadores/', views.indicadorBI, name='indicadorBI'),
    path('cadastro/', views.escSetor, name='escSetor'),
    path('lista_cadastro/<int:idsetor>', views.listaDados, name='listaDados'),
    path('verif_Rel/<int:setor>', views.verifRel, name='verifRel'),
    path('dashboardProctorFiltroPorSetor', views.dashboardProctorFiltroPorSetor, name='dashboardProctorFiltroPorSetor'),
    path('teste/', views.teste, name='teste'),
]


