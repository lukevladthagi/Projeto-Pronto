from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('ficha_identidade/', views.fichaIdentidade, name='ficha_identidade'),
    path('cadastro_gestao/', views.cadastroGestao, name='cadastro_gestao'),
    path('avaliacao_desemp_geral/', views.avaDesempgeral, name='avaliacao_desemp_geral'),
    path('pesquisa_resultado/', views.resultPesquisa, name='pesquisa_resultado'),
    path('avaliacao_competencia/', views.avaliacaoCompetencia, name='avaliacao_competencia'),
    path('auto_avaliacao_competencia/', views.autoAvacomp, name='auto_avaliacao_competencia'),
    path('ava_finalizada/', views.ava_finalizada, name='ava_finalizada'),
    path('relatorio_gestao/', views.relatorio_gestao, name='relatorio_gestao'),
    path('selecionar-trimestre/', views.selecionar_trimestre, name='selecionar-trimestre'),

    #--------------------------NOVO PROCESSO -------------------------------#
    path('pesquisa-colaborador/', views.pesquisaCol, name='pesquisaCol'),
    path('lista_colaborador/<str:nome>', views.listaColaborador, name='listaColaborador'),
    path('ficha_colaborador/<int:id_user>', views.fichaColaborador, name='fichaColaborador'),
    #--------------------NOVO PROCESSO DESEMPENHO GERAL-----------------------#
    path('av_desemp_geral/<int:id_usuario>/<int:id_aval>/<str:id_trimestre>', views.avDesempGeral, name='avDesempGeral'),
    path('avDesGeralFinal/<int:id_usuario>/', views.avDesGeralFinal, name='avDesGeralFinal'),
    #-------------------- NOVO PROCESSO CADASTRO DE METAS (PRODUTIVIDADE) --------------------------#
    path('cadastro_metas/<int:id_usuario>', views.cadastroMetasProdutividade, name='cadastroMetasProdutividade'),
    #--------------------NOVO PROCESSO COMPETENCIA-----------------------#
    path('av_competencia/<int:id_usuario>/<int:id_aval>/<str:id_trimestre>', views.avCompetencia, name='avCompetencia'),
    #--------------------NOVO PROCESSO AUTO-COMPETENCIA-----------------------#
    path('av_auto_competencia/<int:id_usuario>/<int:id_aval>/<str:id_trimestre>', views.autoAvCompetencia, name='autoAvCompetencia'),
    path('ficha_colaborador/', views.fichaColabAuto, name='fichaColabAuto'),
    #--------------------LANÇAMENTO DE META DE PRODUTIVIDADE-------------------#
    path('lanc_meta_produtividade/', views.lancMetaProdut, name='lancMetaProdut'),
    #---------------------RESULTADO DE PROJEÇÕES E METAS----------------------#
    path('resultados/', views.resultadoLanc, name='resultadoLanc'),
    path('resultadosv2/<int:id_usuario>', views.resultadoLancv2, name='resultadoLancv2'),
    
    path('relatorio_gestao/<int:id_usuario>/<int:id_aval>/<str:id_trimestre>', views.relatorio_gestao, name='relatorio_gestao'),
]


