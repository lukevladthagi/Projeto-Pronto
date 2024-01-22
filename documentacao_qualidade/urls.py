from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    #====================================== DOCUMENTOS PUBLICOS =====================================#
    path('documentos-publicos-pastas/', views.pastas_documentacao, name='pastas_documentacao'),
    path('documentos-publicos-arquivos/<int:id_pasta>/', views.pastas_arquivo_documentacao, name='pastas_arquivo_documentacao'),
    #===============================================================================================#
    
    #====================================== DOCUMENTOS QUALIDADE =====================================#
    path('arquivo-por-pasta/<int:id_pasta>/', views.cadastro_arquivos_pastas, name='arquivos_pastas'),
    path('gerenciamento-de-pastas/', views.cadastro_pasta, name='cadastro_pasta'),
    
    #===============================================================================================#
    
    #====================================== CADASTROS EM GERAL =====================================#
    path('cadastro-geral/', views.cadastro_geral, name='cadastro_geral'),
    path('cadastro-tipo-documento/', views.cadastro_tipo_documento, name='cadastro_tipo_documento'),
    path('cadastro-setor-sigla/', views.cadastro_setor_sigla, name='cadastro_setor_sigla'),
    #===============================================================================================#

    #====================================== CENTRAL DA QUALIDADE =====================================#
    path('central-qualidade-documentos/', views.central_qualidade, name='central_qualidade'),
    path('central-qualidade-documentosV2/', views.central_qualidadeV2, name='central_qualidadeV2'),
    path('central-qualidade-documentos/<int:id_solicitacao>/', views.central_qualidade_solicitacao, name='central_qualidade_solicitacao'),
    path('central-qualidade-documentosV2/<int:id_solicitacao>/', views.central_qualidade_solicitacaoV2, name='central_qualidade_solicitacaoV2'),
    #===============================================================================================#

]


