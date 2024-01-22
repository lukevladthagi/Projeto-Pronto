from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.telaInicial, name='telaInicialSistema'),  
    path('login/', views.login, name='login'),
    path('login_chamados/', views.loginChamados, name='login_chamados'), 
    path('logout/', views.logout, name='logout'), 
    path('prontoticket/', include('prontoticket.urls')),
    path('prontocheck/', include('prontocheck.urls')),
    path('prontosaude/', include('prontosaude.urls')),
    path('prontogestao/', include('prontogestao.urls')),
    path('apoioaTI/', include('tecnologia.urls')),
    path('nps/', include('nps.urls')),
    path('controle_agenda/', include('controle_agenda.urls')),
    path('painel_hemodinamica/', include('painel_hemodinamica.urls')),
    path('documentacao_qualidade/', include('documentacao_qualidade.urls')),
    path('acao_estrategica/', include('acao_estrategica.urls')),
    path('plano_orcamentario/', include('plano_orcamentario.urls')),
    path('receituario/', include('receituario.urls')),
    path('reseta/', views.resetaSenha, name='reseta'),
]


