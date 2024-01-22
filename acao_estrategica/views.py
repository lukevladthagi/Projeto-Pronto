from itertools import count
from multiprocessing import context
from administrativo.views import host, apiResponse
from django.shortcuts import render, redirect
import requests, json, pprint, pytz
from datetime import date
from django.views.decorators.cache import cache_page
from datetime import datetime
from dateutil.parser import isoparse
from collections import defaultdict
import calendar
import locale

# Create your views here.


def filtraData(request):
    id_set = request.session.get('id_setor')
    print(f'O seu setor é {id_set}')
    print(30 *'=')
    print('')
    from datetime import datetime
    headers = request.session.get('headers')
    if not headers:
        return render(request, 'pages-error-404.html')
    url_resposta = f'http://{host}/prontocheck/resposta/?setor={id_set[0]}'
    url_setor = f'http://{host}/prontocheck/setor/{id_set}/'
    print(f'a URL  é {url_resposta}')
    print(30 *'=')
    print('')
    response_resposta = requests.get(url=url_resposta, headers=headers)
    response_setor = requests.get(url=url_setor, headers=headers)
    
    data_resposta = response_resposta.json()
    data_resposta2 = response_resposta.json()
    data_setor = response_setor.json()

    meses_distintos_de_respostas = set()
    meses_de_respostas = []

    for resposta in data_resposta:
        item = resposta['created_at']
        data_objeto = isoparse(item)
        data_formatada = data_objeto.strftime("%d-%m-%Y")
        resposta['created_at'] = data_formatada
        mes_da_resposta = resposta['created_at'][:10]
        meses_de_respostas.append(mes_da_resposta)
    meses_distintos_de_respostas = set(meses_de_respostas)

    # Dicionário para armazenar as datas consolidadas
    consolidado = defaultdict(list)

    # Itera sobre as datas, faz o parsing e agrupa por mês e ano
    for data_str in meses_distintos_de_respostas:
        data = datetime.strptime(data_str, '%d-%m-%Y')
        mes_ano = data.strftime('%m-%Y')
        consolidado[mes_ano].append(data_str)

    # Mostra o resultado
    for mes_ano, lista_datas in consolidado.items():
        print(f'{mes_ano}: {lista_datas}')

    if request.method == "POST":
        mes_relat = request.POST.get('mes')
        ano_relat = request.POST.get('ano')
        data_esc = f'{mes_relat}-{ano_relat}'
        
        # Verificar se a chave existe antes de acessar
        if data_esc in consolidado:
            pprint.pprint(f'As datas disponíveis para {data_esc} são: {consolidado[data_esc]}')
            request.session['dt_disponivel'] = consolidado[data_esc]
        else:
            pprint.pprint(f'Não há datas disponíveis para {data_esc}')
            request.session['dt_disponivel'] = consolidado[data_esc]

        return redirect(f'/prontocardio/acao_estrategica/dias-disponiveis/{mes_relat}/{ano_relat}')

    anos = range(2023, 2023 + 10)  # Gera uma lista de anos a partir de 2023 para os próximos 10 anos
    print(list(anos))
    meses = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
    ]
    context = {
        'dias': meses_distintos_de_respostas,
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'meses': meses,
        'anos': anos,
    }
    return render(request, 'seleciona_data.html', context)

def diasDisponiveis(request,mes,ano):
    print(mes)
    print(ano)

    dt_disponivel = request.session.get('dt_disponivel')
    pprint.pprint(dt_disponivel)

    # Configurando o local para português do Brasil
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')

    if request.method == "POST":
        dt_escolhida = request.POST.get('dia')
        print(dt_escolhida)
        return redirect(f'/prontocardio/acao_estrategica/relatorio-gerado/{dt_escolhida}')

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'mes': calendar.month_name[mes],
        'ano': ano,
        'dias':dt_disponivel,
    }
    return render(request, 'dia_disponivel.html',context)

def relatorioGerado(request,dt_esc):
    #Autenticação de login 
    headers = request.session.get('headers')
    id_usu = request.session.get('id_usuario')
    setor = request.session.get('id_setor')
    data = dt_esc
    if not headers:
        return render(request, 'pages-error-404.html')

    urlresp = f'http://{host}/prontocheck/resposta/?setor={setor[0]}'
    urldim =  f'http://{host}/prontocheck/dimensao/?setor={setor[0]}'
    urltitulo =  f'http://{host}/prontocheck/titulo/?setor={setor[0]}'
    urlperg = f'http://{host}/prontocheck/pergunta/?setor={setor[0]}'
    urlset =  f'http://{host}/prontocheck/setor/'
    urlRespEvid =  f'http://{host}/prontocheck/respEvid/'

    response = requests.get(url=urlset, headers=headers)
    response2 = requests.get(url=urlresp, headers=headers)
    response3 = requests.get(url=urldim, headers=headers)
    response4 = requests.get(url=urltitulo, headers=headers)
    response5 = requests.get(url=urlperg, headers=headers)
    responseRespEvid = requests.get(url=urlRespEvid, headers=headers)


    dataset = response.json()
    dataresp = response2.json()
    datadim = response3.json()
    datatit = response4.json()
    dataperg = response5.json()
    dataRespEvid = responseRespEvid.json()



    for item in dataresp:
        dataAbertura = item['created_at']
        dataAbertura = dataAbertura[0:10]
        item['created_at'] = dataAbertura

        dataAbertura = item['created_at']
        data_objeto = datetime.fromisoformat(dataAbertura)
        data_formatada = data_objeto.strftime("%d-%m-%Y")
        item['created_at'] = data_formatada
        mes_da_resposta = item['created_at'][:10]
        item['created_at'] = mes_da_resposta

    for item in dataresp:
        for dimensao in datadim:
            for titulo in datatit:
                for pergunta in dataperg:
                    if item['dimensao'] == dimensao['id']:
                        item['dimensao'] = dimensao['dimensao']
                    if item['titulo'] == titulo['id']:
                        item['titulo'] = titulo['titulo']
                    if item['pergunta'] == pergunta['id']:
                        item['pergunta'] = pergunta['pergunta']


    qt_na_ass = 0
    qt_na_doc = 0
    qt_na_est =0
    qt_na_hot = 0
    qt_na_man =0
    qt_na_pess =0 


    qt_n_ass = 0
    qt_n_doc = 0
    qt_n_est =0
    qt_n_hot = 0
    qt_n_man =0
    qt_n_pess =0 


    qt_s_ass = 0
    qt_s_doc = 0
    qt_s_est =0
    qt_s_hot = 0
    qt_s_man =0
    qt_s_pess =0 
    for resposta in dataresp:
        if resposta['created_at'] == data and resposta['resposta'] == 'sim' and resposta['dimensao'] == 'DIMENSÃO ASSISTENCIAL' :
            #print.pprint(resposta)
            qt_s_ass += 1
        if resposta['created_at'] == data and resposta['resposta'] == 'nao' and resposta['dimensao'] == 'DIMENSÃO ASSISTENCIAL' :
            #print.pprint(resposta)
            qt_n_ass += 1
        if resposta['created_at'] == data and resposta['resposta'] == 'na' and resposta['dimensao'] == 'DIMENSÃO ASSISTENCIAL' :
            #print.pprint(resposta)
            qt_na_ass += 1
        #========================================================#
        if resposta['created_at'] == data and resposta['resposta'] == 'sim' and resposta['dimensao'] == 'DIMENSÃO DOCUMENTOS' :
            #print.pprint(resposta)
            qt_s_doc += 1
        if resposta['created_at'] == data and resposta['resposta'] == 'nao' and resposta['dimensao'] == 'DIMENSÃO DOCUMENTOS' :
            #print.pprint(resposta)
            qt_n_doc += 1
        if resposta['created_at'] == data and resposta['resposta'] == 'na' and resposta['dimensao'] == 'DIMENSÃO DOCUMENTOS' :
            #print.pprint(resposta)
            qt_na_doc += 1
        #===================================================================#
        if resposta['created_at'] == data and resposta['resposta'] == 'sim' and resposta['dimensao'] == 'DIMENSÃO ESTOQUE' :
            #print.pprint(resposta)
            qt_s_est += 1
        if resposta['created_at'] == data and resposta['resposta'] == 'nao' and resposta['dimensao'] == 'DIMENSÃO ESTOQUE' :
            #print.pprint(resposta)
            qt_n_est += 1
        if resposta['created_at'] == data and resposta['resposta'] == 'na' and resposta['dimensao'] == 'DIMENSÃO ESTOQUE' :
            #print.pprint(resposta)
            qt_na_est += 1
        #=======================================================================#
        if resposta['created_at'] == data and resposta['resposta'] == 'sim' and resposta['dimensao'] == 'DIMENSÃO HOTELARIA' :
            #print.pprint(resposta)
            qt_s_hot += 1
        if resposta['created_at'] == data and resposta['resposta'] == 'nao' and resposta['dimensao'] == 'DIMENSÃO HOTELARIA' :
            #print.pprint(resposta)
            qt_n_hot += 1
        if resposta['created_at'] == data and resposta['resposta'] == 'na' and resposta['dimensao'] == 'DIMENSÃO HOTELARIA' :
            #print.pprint(resposta)
            qt_na_hot += 1
        #========================================================================#
        if resposta['created_at'] == data and resposta['resposta'] == 'sim' and resposta['dimensao'] == 'DIMENSÃO MANUTENÇÃO' :
            #print.pprint(resposta)
            qt_s_man += 1
        if resposta['created_at'] == data and resposta['resposta'] == 'nao' and resposta['dimensao'] == 'DIMENSÃO MANUTENÇÃO' :
            #print.pprint(resposta)
            qt_n_man += 1
        if resposta['created_at'] == data and resposta['resposta'] == 'na' and resposta['dimensao'] == 'DIMENSÃO MANUTENÇÃO' :
            #print.pprint(resposta)
            qt_na_man += 1
        #=============================================================================#
        if resposta['created_at'] == data and resposta['resposta'] == 'sim' and resposta['dimensao'] == 'DIMENSÃO PESSOAS' :
            #print.pprint(resposta)
            qt_s_pess += 1
        if resposta['created_at'] == data and resposta['resposta'] == 'nao' and resposta['dimensao'] == 'DIMENSÃO PESSOAS' :
            #print.pprint(resposta)
            qt_n_pess += 1
        if resposta['created_at'] == data and resposta['resposta'] == 'na' and resposta['dimensao'] == 'DIMENSÃO PESSOAS' :
            #print.pprint(resposta)
            qt_na_pess += 1
        #===============================================================================#

    qt_tot_na = qt_na_ass + qt_na_doc + qt_na_est + qt_na_hot + qt_na_man + qt_na_pess
    qt_tot_n = qt_n_ass + qt_n_doc + qt_n_est + qt_n_hot + qt_n_man + qt_n_pess
    qt_tot_s = qt_s_ass + qt_s_doc + qt_s_est + qt_s_hot + qt_s_man + qt_s_pess

    # Calculo qt_tot_ass_porc
    if qt_s_ass + qt_n_ass == 0:
        qt_tot_ass_porc = 0
        qt_tot_ass = '0.00%'
    else:
        qt_tot_ass_porc = (qt_s_ass / (qt_s_ass + qt_n_ass)) * 100
        qt_tot_ass = f'{qt_tot_ass_porc:.2f}%'


    # Calculo qt_tot_doc_porc
    if qt_s_doc + qt_n_doc == 0:
        qt_tot_doc_porc = 0
        qt_tot_doc = '0.00%'
    else:
        qt_tot_doc_porc = (qt_s_doc / (qt_s_doc + qt_n_doc)) * 100
        qt_tot_doc = f'{qt_tot_doc_porc:.2f}%'


    # Calculo qt_tot_est_porc
    if qt_s_est + qt_n_est == 0:
        qt_tot_est_porc = 0
        qt_tot_est = '0.00%'
    else:
        qt_tot_est_porc = (qt_s_est / (qt_s_est + qt_n_est)) * 100
        qt_tot_est = f'{qt_tot_est_porc:.2f}%'


    # Calculo qt_tot_hot_porc
    if qt_s_hot + qt_n_hot == 0:
        qt_tot_hot_porc = 0
        qt_tot_hot = '0.00%'
    else:
        qt_tot_hot_porc = (qt_s_hot / (qt_s_hot + qt_n_hot)) * 100
        qt_tot_hot = f'{qt_tot_hot_porc:.2f}%'


    # Calculo qt_tot_man_porc
    if qt_s_man + qt_n_man == 0:
        qt_tot_man_porc = 0
        qt_tot_man = '0.00%'
    else:
        qt_tot_man_porc = (qt_s_man / (qt_s_man + qt_n_man)) * 100
        qt_tot_man = f'{qt_tot_man_porc:.2f}%'


    # Calculo qt_tot_pess_porc
    if qt_s_pess + qt_n_pess == 0:
        qt_tot_pess_porc = 0
        qt_tot_pess = '0.00%'
    else:
        qt_tot_pess_porc = (qt_s_pess / (qt_s_pess + qt_n_pess)) * 100
        qt_tot_pess = f'{qt_tot_pess_porc:.2f}%'


    # Calculo qt_tot_por
    if qt_tot_s + qt_tot_n == 0:
        qt_tot_por = 0
        qt_tot_tot = '0.00%'
    else:
        qt_tot_por = (qt_tot_s / (qt_tot_s + qt_tot_n)) * 100
        qt_tot_tot = f'{qt_tot_por:.2f}%'

    print(qt_tot_na)
    print(qt_tot_n)
    print(f'Quantidade total sim:{qt_tot_s}')
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'qt_na_ass':qt_na_ass,
        'qt_na_doc':qt_na_doc,
        'qt_na_est':qt_na_est,
        'qt_na_hot':qt_na_hot,
        'qt_na_man':qt_na_man,
        'qt_na_pess':qt_na_pess,
        'qt_tot_na':qt_tot_na,

        'qt_n_ass':qt_n_ass,
        'qt_n_doc':qt_n_doc,
        'qt_n_est':qt_n_est,
        'qt_n_hot':qt_n_hot,
        'qt_n_man':qt_n_man,
        'qt_n_pess':qt_n_pess,
        'qt_tot_n':qt_tot_n,

        'qt_s_ass':qt_s_ass,
        'qt_s_doc':qt_s_doc,
        'qt_s_est':qt_s_est,
        'qt_s_hot':qt_s_hot,
        'qt_s_man':qt_s_man,
        'qt_s_pess':qt_s_pess,
        'qt_tot_s':qt_tot_s,

        'qt_tot_ass':qt_tot_ass,
        'qt_tot_doc':qt_tot_doc,
        'qt_tot_est':qt_tot_est,
        'qt_tot_hot':qt_tot_hot,
        'qt_tot_man':qt_tot_man,
        'qt_tot_pess':qt_tot_pess,
        'qt_tot_tot':qt_tot_tot,
        'respostas':dataresp,
        'dt_esc':data,
        'dimensoes':datadim,
        'titulos':datatit,
        'setores':dataset,
        'imagens':dataRespEvid
    } 
    return render(request, 'relatorio_gerado.html',context)

def planejamentoEstrategico(request,id_resp):
    print('Oi')
    return render(request, 'plan_estrategico.html')