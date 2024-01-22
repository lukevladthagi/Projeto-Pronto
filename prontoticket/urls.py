from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from . import views, utils

urlpatterns = [
    #Abertura de chamado
    path('abrir_chamado/', views.chamado, name='abrir_chamado'),
    path('abrir_chamado_usuario/', views.chamadoUsuario, name='abrir_chamado_usuario'),
    path('pesquisar_chamado/', views.pesquisarChamado, name='pesquisar_chamado'),
    path('pesquisar_chamado_usuario/', views.pesquisarChamadoUsuario, name='pesquisar_chamado_usuario'),
    
    #Agendamento de chamado
    path('agendar_chamado/', views.agendarChamado, name='agendar_chamado'),

    #Confirmação de retorno
    path('confirma_chamado/<int:idchamado>/', views.confirmaChamado, name='confirma_chamado'),
    path('confirma_chamado_usuario/<int:idchamado>/', views.confirmaChamadoUsuario, name='confirma_chamado_usuario'),
    path('nota_realizada_usuario/<int:idchamado>/', views.notaRealizadaUsuario, name='nota_realizada_usuario'),
    path('nota_realizada/<int:idchamado>/', views.notaRealizada, name='nota_realizada'),
    path('atender_finalizar/<int:idchamado>/', views.atenderFinalizar, name='atender_finalizar'),
    
    #Listagem de chamado / Notas
    path('listar_chamado/', views.listarChamado, name='listar_chamado'),
    path('listar_chamado_usuario/', views.listarChamadoUsuario, name='listar_chamado_usuario'),

    #Notas    
    path('nota_informativa/<int:idchamado>/', views.notaInformativa, name='nota_informativa'),
    path('nota_informativa_usuario/<int:idchamado>/', views.notaInformativaUsuario, name='nota_informativa_usuario'),
    
    #Editar chamados
    path('editar_chamado/<int:idchamado>/', views.editarChamado, name='editar_chamado'),
    path('editar_chamado_usuario/<int:idchamado>/', views.editarChamadoUsuario, name='editar_chamado_usuario'),
    path('editar_info/<int:idchamado>/', views.editarInfo, name='editar_info'),
    
    #Dashboard
    path('dash/', views.dash, name='dash'),
    
    #Checklist
    path('redireciona_checklist/', views.setorChecklist, name='redireciona_checklist'),
    path('redireciona_checklist_pt2/<int:idSetor>/', views.setorChecklist_pt2, name='setorChecklist_pt2'),
    path('checklist/<int:idSetor>/<int:local_id>', views.checklist, name='checklist'),
    path('redireciona_cadastro/', views.redirecCad, name='redireciona_cadastro'),
    path('cadastro/<int:id_setor>/', views.checklistCadastro, name='cadastro'),
    path('setor_relatorio/', views.setorRelatorio, name='setor_relatorio'),
    path('redireciona_relatorio/<int:idSetor>/', views.setorRelatorioPt2, name='setorRelatorioPt2'),
    path('relatorio/<int:idSetor>/<str:data>/', views.relatorioEditavel, name='relatorioEditavel'),
    path('relatorio_v2/<int:idSetor>/<str:data>/', views.relatorioConsolidado, name='relatorioConsolidado'),


    #Cadastro técnicos
    path('redireciona_cadtec/', views.redirecionaCadTec, name='redireciona_cadtec'),
    path('cadastro_tec/<int:idSetor>', views.cadastroTec, name='cadastroTec'),

    #Cadastro de Empresas Terceirizadas
    path('cadastro_emp/', views.empresaTerceirizada, name='cadastro_emp'),

    #Cadastro de Sla's
    path('slas/', views.slas, name='slas'),
    path('slas_pt2/<int:idSetor>', views.slas_pt2, name='slas_pt2'),

    #Filtro
    path('filtro/', views.filtroStatus, name='filtro'),

    #Indicador BI TI
    path('indicadorBiTI/', views.indicadorBiTI, name='indicadorBiTI'),
]