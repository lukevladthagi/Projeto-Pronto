from dateutil.parser import isoparse
import requests, json, pprint, pytz
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, timedelta
from administrativo.views import *
import time
#========================= Função Auxiliar Checklist =========================#

def consolidate_dates(data_list):
    meses_de_respostas = set()

    for resposta in data_list:
        item = resposta['criado_em']
        data_objeto = isoparse(item)
        data_formatada = data_objeto.strftime("%d-%m-%Y")
        resposta['criado_em'] = data_formatada
        mes_da_resposta = data_formatada[:10]
        meses_de_respostas.add(mes_da_resposta)

    return meses_de_respostas

def filtrar_json_por_data(json_data, data_desejada):
    # Crie uma lista para armazenar os objetos filtrados
    objetos_filtrados = []
    for objeto in json_data:
        # Converta a data do objeto JSON para um objeto datetime
        data_objeto = datetime.strptime(objeto["criado_em"][:10], "%Y-%m-%d")
        # Converta a data desejada para um objeto datetime
        data_desejada_formatada = datetime.strptime(data_desejada, "%d-%m-%Y")

        # Compare as datas e adicione o objeto à lista se for igual à data desejada
        if data_objeto == data_desejada_formatada:
            objetos_filtrados.append(objeto)

    # Retorne os objetos filtrados como uma resposta JSON
    return objetos_filtrados


def substituir_local(request, array, local):
    local_dict = {item['id']: item['local'] for item in local}

    for item in array:
        if item['local_id'] in local_dict:
            item['local_id'] = local_dict[item['local_id']]

    return array


def get_user_name(request, user_id):
    user_data = apiResponse(request, f'http://{host}/usuarios/{user_id}/', 'GET')
    return user_data.get('nome', '')    

def map_setor_name(chamado, dataSetor):
    for setor in dataSetor:
        if chamado['setor_recebe'] == setor['id']:
            chamado['setor_recebe'] = setor['name']
        
        if chamado['setor_local'] == setor['id']:
            chamado['setor_local'] = setor['name']

def map_problema_name(chamado, dataProblema):
    idProblema = chamado['problema']
    for problema in dataProblema:
        if problema['id'] == idProblema:
            chamado['problema'] = problema['problema']

def map_responsavel_nome(chamado, data_usuario):
    start_time = time.time()
    #Pega o id do item e armazena o nome dele no lugar do id
    id_responsavel = chamado['usuario_atendime']
    
    for item in data_usuario:
        if id_responsavel == item['id']:
            chamado['usuario_atendime'] = item['nome']

    
    end_time = time.time()
    elapsed_time = end_time - start_time

def contar_chamados(request, usuario= None):

    abertos = 0
    andamento = 0
    fechados = 0
    agendados = 0


    #Tratativa de contagem para usuario e tecnico
    if usuario != None:
        dataChamado = apiResponse(request, f'http://{host}/prontoticket/chamado/?usuario={usuario}', 'GET')
        for chamado in dataChamado:
            if chamado['status'] == 2:
                fechados += 1
    
    else:
        bloq_tela = request.session.get('id_setor')
        groups = ', '.join(map(str, bloq_tela))
        dataChamado = apiResponse(request, f'http://{host}/prontoticket/chamados_pendentes/?setor_recebe={groups}', 'GET')
        dataChamadoFinalizado = apiResponse(request, f'http://{host}/prontoticket/chamado/?setor_recebe={groups}', 'GET')
        # Contagem separada de chamados finalizados
        for chamado in dataChamadoFinalizado:
            if chamado['status'] == 2:
                fechados += 1

    # Obtém a data atual
    data_atual = datetime.now()
    mes_atual = data_atual.month
    dia_atual = data_atual.day

    # Inicializa contadores
    
    
    for chamado in dataChamado:
        # Converte a data de criação do chamado para um objeto datetime
        data_criacao = datetime.strptime(chamado['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")

        # Verifica se o chamado está aberto ou fechado
        if chamado['status'] == 1:
            abertos += 1
        if chamado['status'] == 3:
            andamento += 1
        if chamado['status'] == 4:
            agendados += 1
        

    return {
        'abertos': abertos,
        'andamento': andamento,
        'fechados': fechados,
        'agendados': agendados,
    }

def tempo_ocorrido(chamado):
    agendado = chamado['agend']

    if agendado == None:

        now = datetime.now()
        date_string = chamado['created_at']
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        created_at_formated = datetime.strptime(date_string, date_format)
        br_tz = pytz.timezone('America/Sao_Paulo')
        utc_abertura = pytz.utc.localize(created_at_formated)
        br_abertura = utc_abertura.astimezone(br_tz)
        br_abertura = br_abertura.astimezone().replace(tzinfo=None)
        slaDifTime = now - br_abertura

        slaDay = slaDifTime.days
        slaDifTimeStr = str(slaDifTime)
        slaDifTimeStr = slaDifTimeStr[:-7]

        if slaDay == 1:
            slaDifTimeStr = slaDifTimeStr.replace('day', 'dia')

        elif slaDay > 1:
            slaDifTimeStr = slaDifTimeStr.replace('days', 'dias')        


        tcoDelta = slaDifTime
        hours, minutes, seconds = map(int, chamado['m_sla'].split(':'))
        mslaDelta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        if tcoDelta > mslaDelta:
            chamado['updated_at'] = "passou"
    
        return slaDifTimeStr
  
    else:
        agendado = datetime.strptime(agendado, '%Y-%m-%dT%H:%M:%SZ')
        data_agendado = agendado.strftime("%d/%m/%Y, %H:%M")
        return data_agendado
  
def processar_chamados(request, dataChamado, dataSetor, dataProblema, host):
    start_time = time.time()
    data_usuario = apiResponse(request, f'http://{host}/usuarios/', 'GET')
    
    
    for item in dataChamado:

        idUserAtend = item['usuario']
        data_inicio = item['created_at']
        data_alteracao = item['updated_at']
        item['telefone'] = item['created_at']
        item['nome_solicitante'] = get_user_name(request, idUserAtend)
        map_setor_name(item, dataSetor)
        map_problema_name(item, dataProblema)
        map_responsavel_nome(item, data_usuario)
        if item['t_co'] == None or item['t_co'] == '':
            item['t_co'] = tempo_ocorrido(item)
        item['created_at'] = formataData(data_inicio, data_alteracao, "%Y-%m-%dT%H:%M:%S.%fZ")[0]
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time)
    return dataChamado  # Adicionado o retorno da lista de chamados processada

#==================================================================================#
