from cgi import test
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #path('',views.telaInicial, name='telaInicial'),
    path('',views.paciente, name='paciente'),
    path('login/', views.login, name='login'),
    path('marcacao/',views.esc_Agend, name='marcacao'), 
    path('escagendamento/',views.esc_agendamento, name='esc_agendamento'),
    path('convenioExame/',views.convenioExa, name='convenioExa'),
    path('convenioConsulta/',views.convenioCons, name='convenioCons'),
    path('prestador/',views.mostraPrestador, name='prestador'),
    path('especialidade/',views.servico, name='especialidades'), 
    path('horarioconsulta/<int:cdesp>',views.horarioConsulta, name='horarioConsulta'), 
    path('agendar/<int:cdopc>/', views.agendar, name='agendar'),
    path('agendarExames/',views.agendarExames, name='agendarExames'),
    path('exames/',views.mostraExames, name='exames'), 
    path('cadastroPaciente/',views.novoPac, name='cadPac'),
    path('veragendamento/',views.verifcarAgend, name='verifcarAgend'),
    path('cancelaagendamento/',views.cancelaAgenda, name='cancelaAgenda'),
    path('cancelaExame/',views.cancelaExame, name='cancelaExame'),
    path('novoPac/',views.novoPac, name='novoPac'),
    path('informaConvenio/',views.informa_convenio, name='informaConvenio'), 
    path('confirmaAgendamento/', views.confirmaAgend, name= 'confirmaAgend'),
    path('confirmaCancelamento/<int:cdIt>', views.confirmaCancelamento, name= 'confirmaCancelamento'),
    path('confirmaCancelamentoExame/<int:cdIt>', views.confirmaCancelamentoExame, name= 'confirmaCancelamentoExame'),

]


