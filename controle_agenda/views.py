from unittest import result
from django.shortcuts import render
from administrativo.views import host, apiResponse
from django.shortcuts import render, redirect
import requests, json, pprint, pytz
from django.http import JsonResponse
import datetime
import requests
import pprint
from django.http import JsonResponse
from datetime import datetime, timedelta
import multiprocessing
from dateutil.parser import isoparse
from collections import defaultdict
# Create your views here.

TipoAgendamento = ""
Agendamento = ""
TipoAmbulatorio = " "
cnt_pacientes = 0
cnt_pacientes_total_clinica_agora = 0 

eventos_filtrados = {}
resultado2 = {}
tipo_exame = {}
consolidado_por_paciente = {}
 
data_atual = datetime.now().strftime("%Y-%m-%d")
data_hora_atual = datetime.now().strftime("%Y-%m-%d %H")
data_hora_minuto_atual = datetime.now().strftime("%Y-%m-%d %H:%M")
# Obtém a data e hora atual
data_hora_minuto_atual = datetime.now()

# Adiciona 1 hora a essa data e hora
data_hora_minuto_futura = data_hora_minuto_atual + timedelta(hours=1)

c = 0 

# Converte a data e hora futura em uma string no formato dese   jado (YYYY-MM-DD HH:MM)
data_hora_minuto_futura_formatada = data_hora_minuto_futura.strftime("%Y-%m-%d %H:%M")

api_url = "http://192.168.4.48:9090/hpcardio/viewAgendamentoCentral/"

def consolidar_por_prestador(agendamentos):
    consolidado_por_prestador = {}

    for agendamento in agendamentos:
        prestador = agendamento["nm_prestador"]

        if prestador in consolidado_por_prestador:
            consolidado_por_prestador[prestador].append(agendamento)
        else:
            consolidado_por_prestador[prestador] = [agendamento]

    # Organiza o dicionário por ordem alfabética das chaves (nomes dos prestadores)
    consolidado_por_prestador_ordenado = dict(sorted(consolidado_por_prestador.items()))

    return consolidado_por_prestador_ordenado

def consolidar_por_exame(agendamentos):
    consolidado = {}  # Cria um dicionário vazio para consoli dar os dados

    for agendamento in agendamentos:
        exame = agendamento["nm_setor"]  # Obtém o nome do exame

        # Verifica se o nome do exame já está no dicionário
        if exame in consolidado:
            consolidado[exame].append(agendamento)  # Adiciona o agendamento à lista existente
        else:
            consolidado[exame] = [agendamento]  # Cria uma nova lista com o agendamento

    return consolidado

def consolidar_por_tipo(agendamentos):
    consolidado_por_tipo = {} # Cria um dicionário vazio para consolidar os dados
    

    for agendamento in agendamentos:
        tipo_agenda = agendamento["tipo_agenda"]  # Obtém o nome do tipo_agenda

        # Verifica se o nome do tipo_agenda já está no dicionário
        if tipo_agenda in consolidado_por_tipo:

            consolidado_por_tipo[tipo_agenda].append(agendamento)  # Adiciona o agendamento à lista existente
        else:
            consolidado_por_tipo[tipo_agenda] = [agendamento]  # Cria uma nova lista com o agendamento

    return consolidado_por_tipo

# Total de pacientes em 14 dias
def consolidar_por_paciente(agendamentos):
    consolidado_por_paciente = {}
    cnt_pacientes = 0
    cnt_pacientes_total = 0
    
    for agendamento in agendamentos:
        nm_paciente = agendamento["nm_paciente"]  # Obtém o nome do paciente

        # Verifica se o nome do paciente já está no dicionário
        if nm_paciente in consolidado_por_paciente:
            consolidado_por_paciente[nm_paciente].append(agendamento)  # Adiciona o agendamento à lista existente
        else:
            consolidado_por_paciente[nm_paciente] = [agendamento]
            cnt_pacientes_total += 1

    # Retorna uma tupla com cnt_pacientes e consolidado_por_paciente
    return cnt_pacientes, consolidado_por_paciente

def selecionaView(request):
    global TipoAgendamento
    global Agendamento
    global TipoAmbulatorio

    response = requests.get(url=f'{api_url}?search=Ambulatorio')
    response2 = requests.get(url=f'{api_url}?search=Imagem')

    data = response.json()
    data2 = response2.json()
    data3 = response2.json()
    data4 = response2.json()

    resultado = consolidar_por_prestador(data)
    resultado2 = consolidar_por_exame(data2)
    resultado3 = consolidar_por_exame(data3)

    if request.method == "POST":
        request.session['tp_agendamento'] = request.POST.get('TipoAgendamento')
        request.session['agendamento'] = request.POST.get('Agendamentooo')
        request.session['tp_ambulatorio'] = request.POST.get('TipoAmbulatorio')
        print("===========")
        tp_agendamento = request.session.get('tp_agendamento')
        agendamento = request.session.get('agendamento')
        tp_ambulatorio = request.session.get('tp_ambulatorio')
        print(tp_agendamento)
        print(agendamento)
        print(tp_ambulatorio)
        print("=========")
        return redirect(f'../controle_consulta/')

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'prestadores':resultado,
        'exames':resultado2,
        'tipoAgendamento':resultado3,
    }
    return render(request, 'selecionaView.html', context)

def get_events(request):
    response = requests.get(api_url)
    response.raise_for_status() 
    data = response.json()
    eventos_filtrados = []
    global cnt_pacientes_clinica_14dias
    cnt_pacientes_clinica_14dias = 0

    # Itera pelos eventos e atualiza a chave "hr_agenda" com o dia 
    for data in data:      
        if "hr_agenda" in data: 
            hr_agenda = data["hr_agenda"]
            if hr_agenda:
                # Use isoparse para analisar a string de data e hora
                datetime_obj = isoparse(hr_agenda)


                # Formate a data e hora conforme necessário
                formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:00:00")
                
                # Atualize a chave "hr_agenda" no evento com a data formatada
                data["hr_agenda"] = formatted_datetime

        if data['tipo_agenda'] == TipoAgendamento:
            if data['nm_setor'] == Agendamento:
                eventos_filtrados.append(data)
            elif data['nm_prestador'] == Agendamento:
                if data['ds_tip_mar'] == TipoAmbulatorio:
                    eventos_filtrados.append(data)
                if TipoAmbulatorio == "tudo":
                    eventos_filtrados.append(data)
                     
    
    return JsonResponse(eventos_filtrados, safe=False)

def controle_consulta(request):
    headers = request.session.get('headers')
    if not headers:
        return render(request, 'pages-error-404.html')
    #================================================================#
    tp_agendamento = request.session.get('tp_agendamento')
    agendamento = request.session.get('agendamento')
    tp_ambulatorio = request.session.get('tp_ambulatorio')

    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    
    eventos_filtrados = []
    eventsArr = []
    for data in data:      
        if "hr_agenda" in data: 
            hr_agenda = data["hr_agenda"]
            if hr_agenda:
                # Use isoparse para analisar a string de data e hora
                datetime_obj = isoparse(hr_agenda)

                # Formate a data e hora conforme necessário
                formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:00")
                
                # Atualize a chave "hr_agenda" no evento com a data formatada
                data["hr_agenda"] = formatted_datetime
                    
        if data['tipo_agenda'] == tp_agendamento:
            if data['nm_setor'] == agendamento:
                eventos_filtrados.append(data)

            elif data['nm_prestador'] == agendamento:
                if data['ds_tip_mar'] == tp_ambulatorio:
                    eventos_filtrados.append(data)

                if tp_ambulatorio == "tudo":
                    eventos_filtrados.append(data)
        #==============================================================#      
    pprint.pprint(eventos_filtrados)
    #==================== INSERINDO OS DADOS NO ARRAY QUE VAI PRO JS ===================#
    
    for event_data in eventos_filtrados:
        # Verificar se o campo hr_agenda está presente
        if 'hr_agenda' in event_data:
            # Converter a string hr_agenda em um objeto datetime
            date_time = datetime.strptime(event_data['hr_agenda'], '%Y-%m-%d %H:%M:%S')
            # Extrair a data e hora
            date = date_time.date()
            time = date_time.time()

            # Verificar se o campo idade está presente e não é None ou vazio
            if event_data['idade'] == None:
                event_data['idade'] = 00

            event = {
                'day': date.day,
                'month': date.month,
                'year': date.year,
                'events': [
                    {
                        'title': event_data['ds_item_agendamento'],
                        'time': time.strftime('%H:%M:%S'),
                        'insurance': event_data['nm_convenio'],
                        'age': event_data['idade'],
                        'patient_name': event_data['nm_paciente'],
                        'doctor_name': event_data['nm_prestador'],
                        'sector': event_data['nm_setor'],
                        'appointment_type': event_data['tipo_agenda'],
                        'tp_marcacao': event_data['ds_tip_mar'],
                    }
                ],
            }
        eventsArr.append(event)

        patients_count_per_day = {}
        for event in eventsArr:
            date_key = f"{event['year']}-{event['month']}-{event['day']}"
            patients_count_per_day[date_key] = patients_count_per_day.get(date_key, 0) + 1
        
    #===================================================================================#
    
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'cnt_pacientes': cnt_pacientes,  
        'Agendamento': Agendamento,
        'TipoAgendamento': TipoAgendamento,
        'eventsArr': eventsArr,
        'prestador': request.session.get('agendamento'),
        'qnt_pacientes_hoje': len(eventos_filtrados),
        'eventsArr': eventsArr,
    }
    return render (request, 'controle_consulta.html', context)

def selecionaData(request):
    if request.method == "POST":
        request.session['data_inicio_relatorio'] = request.POST.get('data_inicio_relatorio')
        request.session['data_fim_relatorio'] = request.POST.get('data_fim_relatorio')

        data_inicio_relatorio = request.session.get('data_inicio_relatorio')
        data_fim_relatorio = request.session.get('data_fim_relatorio')
        
        print("===========")
        print(data_inicio_relatorio)
        print(data_fim_relatorio)
        print("=========")
        return redirect('../controle_exame/')

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    }
    return render(request, 'selecionaData.html', context)

def controle_exame(request): 
    headers = request.session.get('headers')
    data_inicio_relatorio_str = request.session.get('data_inicio_relatorio')
    data_fim_relatorio_str = request.session.get('data_fim_relatorio')
    
    data_inicio_relatorio = datetime.strptime(data_inicio_relatorio_str, "%Y-%m-%d")
    data_fim_relatorio = datetime.strptime(data_fim_relatorio_str, "%Y-%m-%d")


    #Consumindo a API 
    api_url_total = f"http://192.168.4.48:9090/hpcardio/ViewAgendConsTOT/?start_date={data_inicio_relatorio_str}&end_date={data_fim_relatorio_str}"
    response = requests.get(api_url_total)
    response.raise_for_status() 
    data = response.json()

    #Consumindo api controle cons
    response = requests.get(api_url)
    response.raise_for_status()
    dataCons = response.json()


    #Variavel que armazena os dados filtrados
    eventos_filtrados = []
    exame_cnt = {}
    prestador_cnt = {}
    prestador_p_consulta = {}
    prestador_s_consulta = {}
    prestador_r_consulta = {}
    cnt_primeira_consulta = 0
    cnt_consulta_subsequente = 0
    cnt_consulta_retorno = 0
    qnt_consultas = 0 
    qnt_exames = 0 
    cnt_pacientes_nao_atendido = 0 
    cnt_pacientes_atendidos = 0
    primeira_consulta = {"soma": 0, "datas": []}
    consulta_subsequente = {"soma": 0, "datas": []}
    consulta_retorno = {"soma": 0, "datas": []}
    
    global cnt_pacientes_total_clinica_agora

    if not headers:
        return render(request, 'pages-error-404.html')

    controle_consulta(request)  

    contagem_por_hora = defaultdict(int)


    for data1 in dataCons:
        hr_agenda = data1.get("hr_agenda")
        tipo_agenda = data1.get("tipo_agenda")

        # Verifique se a data é a data atual e se o tipo_agenda é "Ambulatorio"
        if hr_agenda:
            if tipo_agenda == "AMBULATORIO":
                # Use isoparse para analisar a string de data e hora
                datetime_obj = isoparse(hr_agenda)

                # Verifique se a data é a data atual
                if datetime_obj.strftime("%Y-%m-%d") == data_atual:
                    # Formate a data e hora conforme necessário
                    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:00:00")

                    # Atualize a chave "hr_agenda" no evento com a data formatada
                    data1["hr_agenda"] = formatted_datetime

                    # Conte por hora
                    contagem_por_hora[formatted_datetime] += 1

    # Converta o dicionário em um array de objetos
    resultadoCons = [{"hora": chave, "contagem": valor} for chave, valor in contagem_por_hora.items()]

    # Exibindo o resultado
    pprint.pprint(resultadoCons)

       

    #for 
    for data in data: 
        if "ds_tip_mar" in data: 
            if data["ds_tip_mar"] == "Primeira Consulta":
                cnt_primeira_consulta += 1  
            if data["ds_tip_mar"] == "Consulta Subsequente":
                cnt_consulta_subsequente += 1 
            if data["ds_tip_mar"] == "Consulta De Retorno":
                cnt_consulta_retorno +=1  

        if "sn_atendido" in data: 
            if data["sn_atendido"] == "Nao Atendido":
                cnt_pacientes_nao_atendido += 1 
            if data["sn_atendido"] == "Atendido":
                cnt_pacientes_atendidos += 1 
        
        if "tipo_agenda" in data:
            if data["tipo_agenda"] == "Imagem":
                qnt_exames += 1 
            if data["tipo_agenda"] == "Ambulatorio":
                qnt_consultas += 1 

        nm_setor = data["nm_setor"]
        if nm_setor != "Recepcao Clinica":
            if nm_setor in exame_cnt:
                exame_cnt[nm_setor] += 1
            else:
                exame_cnt[nm_setor] = 1
        
        nm_prestador = data["nm_prestador"]
        if nm_prestador:
            if nm_prestador in prestador_cnt:
                prestador_cnt[nm_prestador] += 1
            else:
                prestador_cnt[nm_prestador] = 1

        if data["ds_tip_mar"] == "Primeira Consulta" and nm_prestador:
            if nm_prestador in prestador_p_consulta:
                prestador_p_consulta[nm_prestador] += 1
            else:
                prestador_p_consulta[nm_prestador] = 1

        if data["ds_tip_mar"] == "Consulta Subsequente" and nm_prestador:
            nm_prestador = data["nm_prestador"]
            if nm_prestador in prestador_s_consulta:
                prestador_s_consulta[nm_prestador] += 1
            else:
                prestador_s_consulta[nm_prestador] = 1

        if data["ds_tip_mar"] == "Consulta De Retorno" and nm_prestador:
            nm_prestador = data["nm_prestador"]
            if nm_prestador in prestador_r_consulta:
                prestador_r_consulta[nm_prestador] += 1
            else:
                prestador_r_consulta[nm_prestador] = 1
                

    resto =  42 - cnt_pacientes_total_clinica_agora
    if resto <= 0:
        resto = 0

    cnt_pacientes_total = cnt_pacientes_atendidos + cnt_pacientes_nao_atendido

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'cnt_pacientes_total_clinica_agora': cnt_pacientes_total_clinica_agora,
        'resto': resto,
        'cnt_primeira_consulta': cnt_primeira_consulta,
        'cnt_consulta_subsequente': cnt_consulta_subsequente,
        'cnt_consulta_retorno': cnt_consulta_retorno,
        'qnt_consultas': qnt_consultas,
        'qnt_exames': qnt_exames,
        'cnt_pacientes_nao_atendido': cnt_pacientes_nao_atendido,
        'cnt_pacientes_atendidos': cnt_pacientes_atendidos,
        'cnt_pacientes_total': cnt_pacientes_total,
        'exame_cnt': exame_cnt,
        'prestador_cnt': prestador_cnt,
        'prestador_p_consulta': prestador_p_consulta,
        'prestador_s_consulta': prestador_s_consulta,
        'prestador_r_consulta': prestador_r_consulta,
        'resultadoCons': resultadoCons
    }


    return render (request, 'controle_exame.html', context)