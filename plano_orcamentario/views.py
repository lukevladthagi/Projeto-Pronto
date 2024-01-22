from django.shortcuts import render
from administrativo.views import apiResponse, host, verifica_headers
from django.shortcuts import render, redirect
import requests, json, pprint, pytz, datetime

# Create your views here.

def abertura_orcamento(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
   

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        
    }
    return render(request, 'abertura_orcamento.html', context)

def controle_orcamento(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
   

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        
    }
    return render(request, 'controle_orcamento.html', context)

def dashboard_orcamento(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
   

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        
    }
    return render(request, 'dashboard_orcamento.html', context)

def fechamento_orcamento(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
   

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        
    }
    return render(request, 'fechamento_orcamento.html', context)
