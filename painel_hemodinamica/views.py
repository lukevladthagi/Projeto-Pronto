from django.shortcuts import render
import requests, json, pprint
from django.core.paginator import Paginator
from datetime import date, datetime
from random import randrange
from django.http import JsonResponse
from django.shortcuts import render
from collections import Counter
from collections import defaultdict, OrderedDict
import arrow

# Create your views here.
def painel_hemodinamica(request):

    base_hemodinamica(request)
    
    data_e_hora_em_texto_2 = request.session.get('data_e_hora_em_texto')

    url = 'http://192.168.4.48:9090/paciente_hemodinamica/'
    response = requests.get(url=url)
    dados = response.json()

    data_atual = arrow.now()

    request.session['data_em_texto'] = data_atual.format('DD/MM/YYYY')
    request.session['data_e_hora_em_texto'] = data_atual.format('DD/MM/YYYY')

    data_e_hora_atuais = arrow.now()

    data_em_texto = data_atual.format('DD/MM/YYYY')
    hora_em_texto = data_e_hora_atuais.format('HH:mm')

    #-----------Variaveis contador dia------------------#
    qt_ag_dia = 0
    qt_realz_dia = 0
    qt_cancl_dia = 0

    #-----------Variaveis contador mês------------------#
    qt_ag_mes = 0 
    qt_realz_mes = 0 
    qt_cancl_mes = 0

    #-------------------Mês atual-------------------#
    data_mes_atual = data_atual.format('MM')
    data_mes_ano_atual = data_atual.format('/MM/YYYY')

    #------------------------- Grafico Dia-------------------------------------#
    for item in dados:
        #Pega a quantidade de pacientes agendados no dia
        if item['dt_aviso_cirurgia'] ==  data_em_texto and item['SITUAÇÃO'] == 'Agendada':
            qt_ag_dia += 1

        #Pega a quantidade de pacientes realizados no dia 
        elif item['dt_aviso_cirurgia'] ==  data_em_texto and item['SITUAÇÃO'] == 'Realizada':
            qt_realz_dia += 1

        #Pega a quantidade de pacientes cancelados no dia
        elif item['dt_aviso_cirurgia'] ==  data_em_texto and item['SITUAÇÃO'] == 'Cancelada': 
            qt_cancl_dia += 1

    #--------------------------Mês-------------------------------------#
    for item in dados:
        aviso_cirur = item['dt_aviso_cirurgia']
        aviso_cirur_text = "/" + aviso_cirur[3:10]

        #Pega a quantidade de pacientes cancelados no dia
        if aviso_cirur_text == data_mes_ano_atual and item['SITUAÇÃO'] == 'Cancelada': 
            qt_cancl_mes += 1

        #Pega a quantidade de pacientes realizados no dia 
        elif aviso_cirur_text == data_mes_ano_atual and item['SITUAÇÃO'] == 'Realizada': 
            aviso_cirur = item['dt_aviso_cirurgia']
            aviso_cirur_text = aviso_cirur[3:4] + aviso_cirur[4:5]
            qt_realz_mes += 1

        #Pega a quantidade de pacientes agendados no dia
        elif aviso_cirur_text == data_mes_ano_atual and item['SITUAÇÃO'] == 'Agendada': 
            aviso_cirur = item['dt_aviso_cirurgia']
            aviso_cirur_text = aviso_cirur[3:4] + aviso_cirur[4:5]
            qt_ag_mes += 1

    cnt_meses_ano = 0 
    ano_atual = arrow.now().year

    patients_by_month = OrderedDict()
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    current_year = arrow.now().year

    for month in month_order:
        patients_by_month[month] = 0

    for json_data in dados:
        dt_aviso_cirurgia = arrow.get(json_data["dt_aviso_cirurgia"], 'DD/MM/YYYY')
        situacao = json_data["SITUAÇÃO"]

        # Check if the situation is "Realizada" and surgery date is in the current year before incrementing the count
        if situacao == "Realizada" and dt_aviso_cirurgia.year == current_year:
            patients_by_month[dt_aviso_cirurgia.format('MMM')] += 1

    print(dict(patients_by_month))


    context = {
        'dados': dados,
        'data': data_em_texto,
        'hora': hora_em_texto,
        'qt_agend': qt_ag_dia,
        'qnt_realz': qt_realz_dia,
        'qnt_cancl': qt_cancl_dia,
        'qnt_cancl_mes': qt_cancl_mes,
        'qnt_realz_mes': qt_realz_mes,
        'qnt_ag_mes': qt_ag_mes,
        'patients_by_month': dict(patients_by_month),   
        'data_em_texto': data_e_hora_em_texto_2,  
    }

    return render(request, 'painel.html', context)

def base_hemodinamica(request):
    return render(request, 'base_hemodinamica.html')

