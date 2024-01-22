from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.filtraData, name='filtraData'),
    path('dias-disponiveis/<int:mes>/<int:ano>', views.diasDisponiveis, name='diasDisponiveis'),
    path('relatorio-gerado/<str:dt_esc>', views.relatorioGerado, name='relatorioGerado'),
    path('planejamento-estrategico/<int:id_resp>', views.planejamentoEstrategico, name='planejamentoEstrategico'),
]