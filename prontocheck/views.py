from itertools import count
from multiprocessing import context
from administrativo.views import host, apiResponse
from django.shortcuts import render, redirect
import requests, json, pprint, pytz
from datetime import date
from django.views.decorators.cache import cache_page
from datetime import datetime
from dateutil.parser import isoparse

urlDimensao = f'http://{host}/prontocheck/dimensao/'
urlTitulo = f'http://{host}/prontocheck/titulo/'
urlPergunta = f'http://{host}/prontocheck/pergunta/'
urlSetores = 'http://192.168.4.33:8000/setores/'
urlRespostas = 'http://192.168.4.33:8000/prontocheck/resposta/'
#=======================PRONTOCHECK==============================#

setor_av_id = " "
setor_av_id = 0 

#-------Variaveis cadastro-------------

setorDim = " "
nomeDim = " "

setorEixo = " "
dimenEixo = " "
nomeEixo = " "

setorPerg = " "
dimPerg = " "
eixoPerg = " "
nomePerg = " "
aux = [ ]

# -----------------------------DASHBOARD--------------------------- #

matriz_soma_de_sim = []
matriz_soma_de_nao = []
matriz_soma_de_nao_se_aplica = []
matriz_de_porcentagens_sim = []
matriz_de_porcentagens_nao = []
meses_distintos_de_respostas = []


matriz_soma_de_sim_por_mes_assistencial = []
matriz_soma_de_nao_por_mes_assistencial = []
matriz_de_porcentagens_sim_por_mes_assistencial = []

matriz_soma_de_sim_por_mes_documentos = []
matriz_soma_de_nao_por_mes_documentos = []
matriz_de_porcentagens_sim_por_mes_documentos = []

matriz_soma_de_sim_por_mes_estoque = []
matriz_soma_de_nao_por_mes_estoque = []
matriz_de_porcentagens_sim_por_mes_estoque = []

matriz_soma_de_sim_por_mes_hotelaria = []
matriz_soma_de_nao_por_mes_hotelaria = []
matriz_de_porcentagens_sim_por_mes_hotelaria = []

matriz_soma_de_sim_por_mes_manutencao = []
matriz_soma_de_nao_por_mes_manutencao = []
matriz_de_porcentagens_sim_por_mes_manutencao = []

matriz_soma_de_sim_por_mes_pessoas = []
matriz_soma_de_nao_por_mes_pessoas = []
matriz_de_porcentagens_sim_por_mes_pessoas = []

matriz_de_dimensoes = []
matriz_de_id_dimensoes = []

def filtrar_por_data(data_array, data_alvo):
    objetos_filtrados = []
    data_formatada = datetime.strptime(data_alvo, "%d-%m-%Y")

    for objeto in data_array:
        data_objeto = datetime.strptime(objeto["created_at"][:10], "%Y-%m-%d")
        if data_objeto == data_formatada:
            objetos_filtrados.append(objeto)

    return objetos_filtrados

#---------Relatório----------#

def preRelatoriov2(request):
    headers = request.session.get('headers')
    if not headers:
        return render(request, 'pages-error-404.html')
    urlset =  f'http://{host}/prontocheck/setor/'
    response = requests.get(url=urlset, headers=headers)
    data = response.json()

    if request.method == "POST":
        setor_r = request.POST.get('setor')
        return redirect(f'/prontocardio/prontocheck/prerelatorio2_1/{setor_r}')

    context = {
        'setores': data,
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    return render(request, 'p-relatorio.html', context)

def preRelatoriov2_1(request,id_set):
    from datetime import datetime
    headers = request.session.get('headers')
    if not headers:
        return render(request, 'pages-error-404.html')
    url_resposta = f'http://{host}/prontocheck/resposta/?setor={id_set}'
    url_setor = f'http://{host}/prontocheck/setor/{id_set}/'

    response_resposta = requests.get(url=url_resposta, headers=headers)
    response_setor = requests.get(url=url_setor, headers=headers)
    
    data_resposta = response_resposta.json()
    data_resposta2 = response_resposta.json()
    data_setor = response_setor.json()

    meses_distintos_de_respostas = set()
    meses_de_respostas = []
    if request.method == "POST":
        data_r = request.POST.get('data_relatorio')
        tp_relatorio = request.POST.get('tp_relatorio')
        if tp_relatorio == '1':
            return redirect(f'/prontocardio/prontocheck/relatoriov2/{id_set}/{data_r}')
        if tp_relatorio == '2':
            return redirect(f'/prontocardio/prontocheck/relatorio/{id_set}/{data_r}')
        if tp_relatorio == '3':
            return redirect(f'/prontocardio/prontocheck/relatoriov3/{id_set}/{data_r}')
    for resposta in data_resposta:
        item = resposta['created_at']
        data_objeto = isoparse(item)
        data_formatada = data_objeto.strftime("%d-%m-%Y")
        resposta['created_at'] = data_formatada
        mes_da_resposta = resposta['created_at'][:10]
        meses_de_respostas.append(mes_da_resposta)
    meses_distintos_de_respostas = set(meses_de_respostas)

    context = {
        'dias': meses_distintos_de_respostas,
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'setor_id':id_set,
        'setores':data_setor

    }
    return render(request, 'p-relatorio2.1.html', context)

def relatorio(request,setor,data):
    headers = request.session.get('headers')
    id_usu = request.session.get('id_usuario')
    if not headers:
        return render(request, 'pages-error-404.html')

    urlresp = f'http://{host}/prontocheck/resposta/?setor={setor}'
    urldim =  f'http://{host}/prontocheck/dimensao/?setor={setor}'
    urltitulo =  f'http://{host}/prontocheck/titulo/?setor={setor}'
    urlperg = f'http://{host}/prontocheck/pergunta/?setor={setor}'
    urlset =  f'http://{host}/prontocheck/setor/{setor}/'
    urlset2 =  f'http://{host}/prontocheck/setor/'
    urlRespEvid =  f'http://{host}/prontocheck/respEvid/'

    responseSetor = requests.get(url=urlset, headers=headers)
    responseSetor2 = requests.get(url=urlset2, headers=headers)
    responseResp = requests.get(url=urlresp, headers=headers)
    responseDimensao = requests.get(url=urldim, headers=headers)
    responseTitulo = requests.get(url=urltitulo, headers=headers)
    responsePergunta = requests.get(url=urlperg, headers=headers)
    responseRespEvid = requests.get(url=urlRespEvid, headers=headers)

    dataSetor = responseSetor.json()
    dataSetor2 = responseSetor2.json()
    dataResp = responseResp.json()
    dataDimensao = responseDimensao.json()
    dataTitulo = responseTitulo.json()
    dataPergunta = responsePergunta.json()
    dataRespEvid = responseRespEvid.json()

    #----Filtro de respostas---------------------#
    data_filtrada = filtrar_por_data(dataResp, data)
    pprint.pprint(data_filtrada)
    
    #=========FUNÇÃO PARA DELETAR VÁRIAS RESPOSTAS==========#
    #var1 = delete_objects(request, data_filtrada)
    #print(var1)
    #=======================================================#

    #---Altera o tipo da data----#
    for item in data_filtrada:
        dataAbertura = item['created_at']
        dataAbertura = dataAbertura[0:10]
        item['created_at'] = dataAbertura

        dataAbertura = item['created_at']
        data_objeto = datetime.fromisoformat(dataAbertura)
        data_formatada = data_objeto.strftime("%d-%m-%Y")
        item['created_at'] = data_formatada
        mes_da_resposta = item['created_at'][:10]
        item['created_at'] = mes_da_resposta
    #-----------------------------#
    if request.method == "POST":

        if '_method' in request.POST and request.POST['_method'] == 'DELETE':
            id_resp = request.POST.get('id_resp')
            print(f"{urlRespostas}{id_resp}/")
            responsedel = apiResponse(request,f"{urlRespostas}{id_resp}/",'DEL')
            print(responsedel)
            print('Apagado')
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'FOTOS':
            id_resp = request.POST.get('id_resp')
            fotos_selecionadas = request.POST.getlist('fotos[]')

            for foto_id in fotos_selecionadas:
                # Enviar solicitação DELETE para a API para excluir a foto
                url_delete_foto = f'http://{host}/prontocheck/respEvid/{foto_id}/'  # Substitua pela URL correta da sua API
                responsedel = requests.delete(url=url_delete_foto, headers=headers)

                if responsedel.status_code == 204:
                    # A foto foi excluída com sucesso
                    print(f'Foto {foto_id} excluída com sucesso.')
                else:
                    # Ocorreu um erro ao excluir a foto, exibir a mensagem de erro
                    print(f'Falha ao excluir a foto {foto_id}. Erro: {responsedel.text}')

            files2 = request.FILES.getlist('evidencia')  # Obter a lista de arquivos enviados
            resposta_id = request.POST.get('id_resp')
            
            print(resposta_id)

            for file in files2:
                data_body = {'resposta': resposta_id}  # Dados adicionais para enviar junto com a foto
                files = {"evidencia": file}  # Arquivo a ser enviado
                response = requests.post(urlRespEvid, files=files, data=data_body, headers=headers)
                if response.status_code == 201:
                    # A foto foi enviada com sucesso
                    print(f'Foto {file.name} enviada com sucesso.')
                else:
                    # O envio falhou para esta foto, exibir a mensagem de erro
                    print(f'Falha ao enviar a foto {file.name}. Erro: {response.text}')
        if '_method' in request.POST and request.POST['_method'] == 'EDITAR':
            print('Editar resposta')
            body_edit = {
                "user": id_usu
            }
            resp_id = request.POST.get('id_resp')
            resposta = request.POST.get('resposta')
            comentario = request.POST.get('comentario')
            evidencia = request.FILES.get('evidencia')
            a_res = request.POST.get('arearesponsavel')

            if comentario is not None and comentario.strip() != '':
                body_edit["comentario"] = comentario
            if resposta is not None and resposta.strip() != '':
                body_edit["resposta"] = resposta
            if evidencia is not None:
                files = {"evidencia": evidencia}
            else:
                files = None

            if a_res is not None and a_res.strip() != '':
                body_edit["a_resp"] = a_res
            response = requests.put(url=f"{urlRespostas}{resp_id}/", data=body_edit, files=files, headers=headers)
            data = response.json()
            return redirect(request.path)
    context = {
        'dimensaos': dataDimensao,
        'titulos': dataTitulo,
        'perguntas': dataPergunta,
        'respostas': data_filtrada,
        'setor_esc': int(setor),
        'dt_esc': str(data),
        'nome_setor': dataSetor['name'],
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'setores': dataSetor2,
        'imagens':dataRespEvid
    } 
    return render(request, 'relatorio-gerado.html', context)

def relatoriov2(request,setor,data):
    #Autenticação de login 
    global setor_r
    global armazena_nome_S
    headers = request.session.get('headers')
    id_usu = request.session.get('id_usuario')
    if not headers:
        return render(request, 'pages-error-404.html')

    urlresp = f'http://{host}/prontocheck/resposta/?setor={setor}'
    urldim =  f'http://{host}/prontocheck/dimensao/?setor={setor}'
    urltitulo =  f'http://{host}/prontocheck/titulo/?setor={setor}'
    urlperg = f'http://{host}/prontocheck/pergunta/?setor={setor}'
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



    for nome_setor in dataset:
        if nome_setor['id'] == int(setor):
            armazena_nome_S = nome_setor['name']

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


    context = {
        'armazena_nome_S': armazena_nome_S,
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
    return render(request, 'relatorio-geradov2.html', context)

def relatoriov3(request,setor,data):
    #Autenticação de login 
    global setor_r
    global armazena_nome_S
    headers = request.session.get('headers')
    id_usu = request.session.get('id_usuario')
    if not headers:
        return render(request, 'pages-error-404.html')

    urlresp = f'http://{host}/prontocheck/resposta/?setor={setor}'
    urldim =  f'http://{host}/prontocheck/dimensao/?setor={setor}'
    urltitulo =  f'http://{host}/prontocheck/titulo/?setor={setor}'
    urlperg = f'http://{host}/prontocheck/pergunta/?setor={setor}'
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


    for nome_setor in dataset:
        if nome_setor['id'] == int(setor):
            armazena_nome_S = nome_setor['name']

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


    peso_ass = 0
    peso_doc = 0
    peso_est = 0
    peso_hot = 0
    peso_man = 0
    peso_pess = 0

    for item in datadim:
        if item['dimensao'] == 'DIMENSÃO ASSISTENCIAL':
            peso_ass = item['peso']
        if item['dimensao'] == 'DIMENSÃO DOCUMENTOS':
            peso_doc = item['peso']
        if item['dimensao'] == 'DIMENSÃO ESTOQUE':
            peso_est = item['peso']
        if item['dimensao'] == 'DIMENSÃO HOTELARIA':
            peso_hot = item['peso']
        if item['dimensao'] == 'DIMENSÃO MANUTENÇÃO':
            peso_man = item['peso']
        if item['dimensao'] == 'DIMENSÃO PESSOAS':
            peso_pess = item['peso']

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
    qt_tot_s_peso = 0

    #for item in datadim:
    #    qt_tot_s_peso = (int(item['peso'])*qt_s_ass+)
    #    pprint.pprint(f"{item['dimensao']}:PESO={item['peso']}")

    

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
        qt_tot_peso_s = (peso_ass*qt_s_ass + peso_pess*qt_s_pess + peso_doc*qt_s_doc + peso_est*qt_s_est + peso_man*qt_s_man + peso_hot*qt_s_hot)
        qt_tot_peso = ((peso_ass*(qt_s_ass+qt_n_ass)) + (peso_pess*(qt_s_pess+qt_n_pess)) + (peso_doc*(qt_s_doc+qt_n_doc)) + (peso_est*(qt_s_est+qt_n_est)) + (peso_man*(qt_s_man+qt_n_man)) + (peso_hot*(qt_s_hot+qt_n_hot)))
        
        print("=" * 20)
        print(f'Peso assistência:{peso_ass} \nPeso Pessoa:{peso_pess} \nPeso Documento:{peso_doc} \nPeso Estoque:{peso_est} \nPeso Manutenção:{peso_man} \nPeso Hotelaria:{peso_hot} ')
        print('-' * 20)
        print(f'Qtd_ass(SIM):{qt_s_ass}\nQtd_pess(SIM):{qt_s_pess}\nQtd_Doc(SIM):{qt_s_doc}\nQtd_Estq(SIM):{qt_s_est}\nQtd_Manut(SIM):{qt_s_man}\nQtd_Hotel(SIM):{qt_s_hot}')
        print("=" * 20)

        resultado = (qt_tot_peso_s / qt_tot_peso) * 100

        print(f'Total de SIM com peso:{qt_tot_peso_s}')
        print(f'Total com peso:{qt_tot_peso}')

        qt_tot_tot = f'{resultado:.2f}%'

    context = {
        'armazena_nome_S': armazena_nome_S,
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
        'imagens':dataRespEvid,

        'peso_ass':peso_ass,
        'peso_doc':peso_doc,
        'peso_est':peso_est,
        'peso_hot':peso_hot,
        'peso_man':peso_man,
        'peso_pess':peso_pess,

    } 
    return render(request, 'relatorio-geradov3.html', context)





def relatorio_erro(request):
    if not headers:
        return render(request, 'pages-error-404.html')
    return render(request, 'relatorio_erro.html')

def dashboardProctor(request):
    global setor_escolhido
    global data_inicial_escolhida
    global data_final_escolhida

    global matriz_soma_de_sim
    global matriz_soma_de_nao
    global matriz_soma_de_nao_se_aplica
    global matriz_de_porcentagens_sim
    global matriz_de_porcentagens_nao
    global meses_distintos_de_respostas


    global matriz_soma_de_sim_por_mes_assistencial
    global matriz_soma_de_nao_por_mes_assistencial
    global matriz_de_porcentagens_sim_por_mes_assistencial

    global matriz_soma_de_sim_por_mes_documentos
    global matriz_soma_de_nao_por_mes_documentos
    global matriz_de_porcentagens_sim_por_mes_documentos

    global matriz_soma_de_sim_por_mes_estoque
    global matriz_soma_de_nao_por_mes_estoque
    global matriz_de_porcentagens_sim_por_mes_estoque

    global matriz_soma_de_sim_por_mes_hotelaria
    global matriz_soma_de_nao_por_mes_hotelaria
    global matriz_de_porcentagens_sim_por_mes_hotelaria

    global matriz_soma_de_sim_por_mes_manutencao
    global matriz_soma_de_nao_por_mes_manutencao
    global matriz_de_porcentagens_sim_por_mes_manutencao

    global matriz_soma_de_sim_por_mes_pessoas
    global matriz_soma_de_nao_por_mes_pessoas
    global matriz_de_porcentagens_sim_por_mes_pessoas

    global matriz_de_dimensoes
    global matriz_de_id_dimensoes
    

    headers = request.session.get('headers')
    if not headers:
        return render(request, 'pages-error-404.html')

    if request.method == "POST":
        setor_escolhido = request.POST.get('setor')
        data_inicial_escolhida = request.POST.get('data_relatorio_inicial')
        data_final_escolhida = request.POST.get('data_relatorio_final')
        
        ano_data_inicial_escolhida = data_inicial_escolhida[0:4]
        mes_data_inicial_escolhida = data_inicial_escolhida[5:7]
        dia_data_inicial_escolhida = data_inicial_escolhida[8:10]
        string_da_data_inicial_escolhida = dia_data_inicial_escolhida + "/"  + mes_data_inicial_escolhida + "/" + ano_data_inicial_escolhida
        numero_da_data_inicial_escolhida = int(ano_data_inicial_escolhida + mes_data_inicial_escolhida + dia_data_inicial_escolhida)

        ano_data_final_escolhida = data_final_escolhida[0:4]
        mes_data_final_escolhida = data_final_escolhida[5:7]
        dia_data_final_escolhida = data_final_escolhida[8:10]
        string_da_data_final_escolhida = dia_data_final_escolhida + "/"  + mes_data_final_escolhida + "/" + ano_data_final_escolhida
        numero_da_data_final_escolhida = int(ano_data_final_escolhida + mes_data_final_escolhida + dia_data_final_escolhida)

        url_resposta = f'http://{host}/prontocheck/resposta/'
        url_dimensao =  f'http://{host}/prontocheck/dimensao/'
        url_setor = f'http://{host}/setores/'
        # url_setor =  f'http://{host}/prontocheck/setor/'
        url_titulo =  f'http://{host}/prontocheck/titulo/'
        url_pergunta = f'http://{host}/prontocheck/pergunta/'

        response_setor = requests.get(url=url_setor, headers=headers)
        response_resposta = requests.get(url=url_resposta, headers=headers)
        response_dimensao = requests.get(url=url_dimensao, headers=headers)
        response_titulo = requests.get(url=url_titulo, headers=headers)
        response_pergunta = requests.get(url=url_pergunta, headers=headers)

        data_setor = response_setor.json()
        data_resposta = response_resposta.json()
        data_dimensao = response_dimensao.json()
        data_titulo = response_titulo.json()
        data_pergunta = response_pergunta.json()

        matriz_soma_de_sim = []
        matriz_soma_de_nao = []
        matriz_soma_de_nao_se_aplica = []
        matriz_de_porcentagens_sim = []
        matriz_de_porcentagens_nao = []
        meses_distintos_de_respostas = []

        matriz_soma_de_sim_por_mes_assistencial = []
        matriz_soma_de_nao_por_mes_assistencial = []
        matriz_de_porcentagens_sim_por_mes_assistencial = []

        matriz_soma_de_sim_por_mes_documentos = []
        matriz_soma_de_nao_por_mes_documentos = []
        matriz_de_porcentagens_sim_por_mes_documentos = []

        matriz_soma_de_sim_por_mes_estoque = []
        matriz_soma_de_nao_por_mes_estoque = []
        matriz_de_porcentagens_sim_por_mes_estoque = []

        matriz_soma_de_sim_por_mes_hotelaria = []
        matriz_soma_de_nao_por_mes_hotelaria = []
        matriz_de_porcentagens_sim_por_mes_hotelaria = []

        matriz_soma_de_sim_por_mes_manutencao = []
        matriz_soma_de_nao_por_mes_manutencao = []
        matriz_de_porcentagens_sim_por_mes_manutencao = []

        matriz_soma_de_sim_por_mes_pessoas = []
        matriz_soma_de_nao_por_mes_pessoas = []
        matriz_de_porcentagens_sim_por_mes_pessoas = []

        matriz_de_dimensoes = []
        matriz_de_id_dimensoes = []
        
        for setor in data_setor:
            if setor['id'] == int(setor_escolhido):
                nome_do_setor_escolhido = setor['name']

        dimensoes = []
        lista_de_dimensoes_distintas = []
        for dimensao in data_dimensao:
            dimensoes.append(dimensao['dimensao'])
        dimensoes = set(dimensoes)

        for dimensao in dimensoes:
            lista_de_dimensoes_distintas.append(dimensao)

        quantidade_de_setores = len(data_setor)
        quantidade_de_dimensoes = len(lista_de_dimensoes_distintas)

        matriz_de_id_dimensoes = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_sim = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_se_aplica = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_dimensoes = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_nao = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
 
        meses_de_respostas = []
        ano_de_respostas = []
        for resposta in data_resposta:
            mes_da_resposta = resposta['created_at']
            mes_da_resposta = mes_da_resposta[0:7]
            ano_da_resposta = mes_da_resposta[3:7]
            ano_de_respostas.append(ano_da_resposta)
            meses_de_respostas.append(mes_da_resposta)

        meses_de_respostas = set(meses_de_respostas)
        ano_de_respostas = set(ano_de_respostas)
        quantidade_de_anos = len(ano_de_respostas)

        for mes in meses_de_respostas:
            meses_distintos_de_respostas.append(mes)
        
        quantidade_de_meses = len(meses_distintos_de_respostas)
        todos_os_meses_do_ano = []
        for ano in ano_de_respostas:
            for _ in range(13):
                mes = 1
                mes_e_ano = mes + "-" + ano
                if (len(mes_e_ano)==6):
                    mes_e_ano = "0" + mes_e_ano
                todos_os_meses_do_ano.append(mes_e_ano)
                mes = mes + 1
        print(todos_os_meses_do_ano)
        matriz_soma_de_sim_por_mes_assistencial = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_por_mes_assistencial = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim_por_mes_assistencial = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]

        matriz_soma_de_sim_por_mes_documentos = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_por_mes_documentos = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim_por_mes_documentos = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]

        matriz_soma_de_sim_por_mes_estoque = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_por_mes_estoque = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim_por_mes_estoque = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]

        matriz_soma_de_sim_por_mes_hotelaria = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_por_mes_hotelaria = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim_por_mes_hotelaria = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)] 

        matriz_soma_de_sim_por_mes_manutencao = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_por_mes_manutencao = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim_por_mes_manutencao = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]

        matriz_soma_de_sim_por_mes_pessoas = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_por_mes_pessoas = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim_por_mes_pessoas = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]

        for setor in data_setor:
            for dimensao in data_dimensao:
                if dimensao['setor'] == setor['id']:
                    if dimensao['dimensao'] == 'DIMENSÃO ASSISTENCIAL':
                        matriz_soma_de_sim_por_mes_assistencial[setor['id']][0] = dimensao['id']
                        matriz_soma_de_nao_por_mes_assistencial[setor['id']][0] = dimensao['id']                        
                        matriz_de_porcentagens_sim_por_mes_assistencial[setor['id']][0] = dimensao['id']
                    if dimensao['dimensao'] == 'DIMENSÃO DOCUMENTOS':
                        matriz_soma_de_sim_por_mes_documentos[setor['id']][0] = dimensao['id']
                        matriz_soma_de_nao_por_mes_documentos[setor['id']][0] = dimensao['id']                        
                        matriz_de_porcentagens_sim_por_mes_documentos[setor['id']][0] = dimensao['id']
                    if dimensao['dimensao'] == 'DIMENSÃO ESTOQUE':
                        matriz_soma_de_sim_por_mes_estoque[setor['id']][0] = dimensao['id']
                        matriz_soma_de_nao_por_mes_estoque[setor['id']][0] = dimensao['id']                        
                        matriz_de_porcentagens_sim_por_mes_estoque[setor['id']][0] = dimensao['id']
                    if dimensao['dimensao'] == 'DIMENSÃO HOTELARIA':
                        matriz_soma_de_sim_por_mes_hotelaria[setor['id']][0] = dimensao['id']
                        matriz_soma_de_nao_por_mes_hotelaria[setor['id']][0] = dimensao['id']                        
                        matriz_de_porcentagens_sim_por_mes_hotelaria[setor['id']][0] = dimensao['id']
                    if dimensao['dimensao'] == 'DIMENSÃO MANUTENÇÃO':
                        matriz_soma_de_sim_por_mes_manutencao[setor['id']][0] = dimensao['id']
                        matriz_soma_de_nao_por_mes_manutencao[setor['id']][0] = dimensao['id']                        
                        matriz_de_porcentagens_sim_por_mes_manutencao[setor['id']][0] = dimensao['id']
                    if dimensao['dimensao'] == 'DIMENSÃO PESSOAS':
                        matriz_soma_de_sim_por_mes_pessoas[setor['id']][0] = dimensao['id']
                        matriz_soma_de_nao_por_mes_pessoas[setor['id']][0] = dimensao['id']                        
                        matriz_de_porcentagens_sim_por_mes_pessoas[setor['id']][0] = dimensao['id']

        for resposta in data_resposta:
            for setor in data_setor:
                if resposta['setor'] == setor['id']:
                    for i in range(0,len(meses_de_respostas)):
                        mes_da_resposta = resposta['created_at']
                        mes_da_resposta = mes_da_resposta[0:7]
                        if meses_distintos_de_respostas[i] == mes_da_resposta:
                            if resposta['dimensao'] == matriz_soma_de_sim_por_mes_assistencial[setor['id']][0]:
                                if resposta['resposta'] == "sim":
                                    matriz_soma_de_sim_por_mes_assistencial[setor['id']][i+1] = matriz_soma_de_sim_por_mes_assistencial[setor['id']][i+1] + 1
                                if resposta['resposta'] == "nao":
                                    matriz_soma_de_nao_por_mes_assistencial[setor['id']][i+1] = matriz_soma_de_nao_por_mes_assistencial[setor['id']][i+1] + 1
                            if resposta['dimensao'] == matriz_soma_de_sim_por_mes_documentos[setor['id']][0]:
                                if resposta['resposta'] == "sim":
                                    matriz_soma_de_sim_por_mes_documentos[setor['id']][i+1] = matriz_soma_de_sim_por_mes_documentos[setor['id']][i+1] + 1
                                if resposta['resposta'] == "nao":
                                    matriz_soma_de_nao_por_mes_documentos[setor['id']][i+1] = matriz_soma_de_nao_por_mes_documentos[setor['id']][i+1] + 1
                            if resposta['dimensao'] == matriz_soma_de_sim_por_mes_estoque[setor['id']][0]:
                                if resposta['resposta'] == "sim":
                                    matriz_soma_de_sim_por_mes_estoque[setor['id']][i+1] = matriz_soma_de_sim_por_mes_estoque[setor['id']][i+1] + 1
                                if resposta['resposta'] == "nao":
                                    matriz_soma_de_nao_por_mes_estoque[setor['id']][i+1] = matriz_soma_de_nao_por_mes_estoque[setor['id']][i+1] + 1
                            if resposta['dimensao'] == matriz_soma_de_sim_por_mes_hotelaria[setor['id']][0]:
                                if resposta['resposta'] == "sim":
                                    matriz_soma_de_sim_por_mes_hotelaria[setor['id']][i+1] = matriz_soma_de_sim_por_mes_hotelaria[setor['id']][i+1] + 1
                                if resposta['resposta'] == "nao":
                                    matriz_soma_de_nao_por_mes_hotelaria[setor['id']][i+1] = matriz_soma_de_nao_por_mes_hotelaria[setor['id']][i+1] + 1
                            if resposta['dimensao'] == matriz_soma_de_sim_por_mes_manutencao[setor['id']][0]:
                                if resposta['resposta'] == "sim":
                                    matriz_soma_de_sim_por_mes_manutencao[setor['id']][i+1] = matriz_soma_de_sim_por_mes_manutencao[setor['id']][i+1] + 1
                                if resposta['resposta'] == "nao":
                                    matriz_soma_de_nao_por_mes_manutencao[setor['id']][i+1] = matriz_soma_de_nao_por_mes_manutencao[setor['id']][i+1] + 1
                            if resposta['dimensao'] == matriz_soma_de_sim_por_mes_pessoas[setor['id']][0]:
                                if resposta['resposta'] == "sim":
                                    matriz_soma_de_sim_por_mes_pessoas[setor['id']][i+1] = matriz_soma_de_sim_por_mes_pessoas[setor['id']][i+1] + 1
                                if resposta['resposta'] == "nao":
                                    matriz_soma_de_nao_por_mes_pessoas[setor['id']][i+1] = matriz_soma_de_nao_por_mes_pessoas[setor['id']][i+1] + 1
 

        for i in range(0,quantidade_de_setores+1):
            for j in range(1,len(meses_de_respostas)+1):
                if matriz_soma_de_sim_por_mes_assistencial[i][j]+matriz_soma_de_nao_por_mes_assistencial[i][j] != 0:
                    matriz_de_porcentagens_sim_por_mes_assistencial[i][j] = round((matriz_soma_de_sim_por_mes_assistencial[i][j]/(matriz_soma_de_sim_por_mes_assistencial[i][j]+matriz_soma_de_nao_por_mes_assistencial[i][j]))*100, 2) 
                if matriz_soma_de_sim_por_mes_documentos[i][j]+matriz_soma_de_nao_por_mes_documentos[i][j] != 0:
                    matriz_de_porcentagens_sim_por_mes_documentos[i][j] = round((matriz_soma_de_sim_por_mes_documentos[i][j]/(matriz_soma_de_sim_por_mes_documentos[i][j]+matriz_soma_de_nao_por_mes_documentos[i][j]))*100, 2) 
                if matriz_soma_de_sim_por_mes_estoque[i][j]+matriz_soma_de_nao_por_mes_estoque[i][j] != 0:
                    matriz_de_porcentagens_sim_por_mes_estoque[i][j] = round((matriz_soma_de_sim_por_mes_estoque[i][j]/(matriz_soma_de_sim_por_mes_estoque[i][j]+matriz_soma_de_nao_por_mes_estoque[i][j]))*100, 2) 
                if matriz_soma_de_sim_por_mes_hotelaria[i][j]+matriz_soma_de_nao_por_mes_hotelaria[i][j] != 0:
                    matriz_de_porcentagens_sim_por_mes_hotelaria[i][j] = round((matriz_soma_de_sim_por_mes_hotelaria[i][j]/(matriz_soma_de_sim_por_mes_hotelaria[i][j]+matriz_soma_de_nao_por_mes_hotelaria[i][j]))*100, 2) 
                if matriz_soma_de_sim_por_mes_manutencao[i][j]+matriz_soma_de_nao_por_mes_manutencao[i][j] != 0:
                    matriz_de_porcentagens_sim_por_mes_manutencao[i][j] = round((matriz_soma_de_sim_por_mes_manutencao[i][j]/(matriz_soma_de_sim_por_mes_manutencao[i][j]+matriz_soma_de_nao_por_mes_manutencao[i][j]))*100, 2) 
                if matriz_soma_de_sim_por_mes_pessoas[i][j]+matriz_soma_de_nao_por_mes_pessoas[i][j] != 0:                    
                    matriz_de_porcentagens_sim_por_mes_pessoas[i][j] = round((matriz_soma_de_sim_por_mes_pessoas[i][j]/(matriz_soma_de_sim_por_mes_pessoas[i][j]+matriz_soma_de_nao_por_mes_pessoas[i][j]))*100, 2) 

        for resposta in data_resposta:
            dataAbertura = resposta['created_at']
            dataAbertura = dataAbertura[0:10]
            resposta['created_at'] = dataAbertura

        for setor in data_setor:
            for dimensao in data_dimensao:
                if dimensao['setor'] == setor['id']:
                    if dimensao['dimensao'] == 'DIMENSÃO ASSISTENCIAL':
                        matriz_de_dimensoes[setor['id']][1] = 'DIMENSÃO ASSISTENCIAL'
                        matriz_de_id_dimensoes[setor['id']][1] = dimensao['id']
                    if dimensao['dimensao'] == 'DIMENSÃO DOCUMENTOS':
                        matriz_de_dimensoes[setor['id']][2] = 'DIMENSÃO DOCUMENTOS'
                        matriz_de_id_dimensoes[setor['id']][2] = dimensao['id']
                    if dimensao['dimensao'] == 'DIMENSÃO ESTOQUE':
                        matriz_de_dimensoes[setor['id']][3] = 'DIMENSÃO ESTOQUE'
                        matriz_de_id_dimensoes[setor['id']][3] = dimensao['id']
                    if dimensao['dimensao'] == 'DIMENSÃO HOTELARIA':
                        matriz_de_dimensoes[setor['id']][4] = 'DIMENSÃO HOTELARIA'
                        matriz_de_id_dimensoes[setor['id']][4] = dimensao['id']
                    if dimensao['dimensao'] == 'DIMENSÃO MANUTENÇÃO':
                        matriz_de_dimensoes[setor['id']][5] = 'DIMENSÃO MANUTENÇÃO'
                        matriz_de_id_dimensoes[setor['id']][5] = dimensao['id']
                    if dimensao['dimensao'] == 'DIMENSÃO PESSOAS':
                        matriz_de_dimensoes[setor['id']][6] = 'DIMENSÃO PESSOAS'
                        matriz_de_id_dimensoes[setor['id']][6] = dimensao['id']


        for resposta in data_resposta:
            ano_resposta = resposta['created_at'][0:4]
            mes_resposta = resposta['created_at'][5:7]
            dia_resposta = resposta['created_at'][8:10]
            numero_da_data_resposta = int(ano_resposta + mes_resposta + dia_resposta)
            if numero_da_data_inicial_escolhida <= numero_da_data_resposta and numero_da_data_resposta <= numero_da_data_final_escolhida:
                for setor in data_setor:
                    if resposta['setor'] == setor['id']:
                        for i in range(0,quantidade_de_dimensoes+1):
                            if matriz_de_id_dimensoes[setor['id']][i] == resposta['dimensao']:
                                if resposta['resposta'] == "sim":
                                    matriz_soma_de_sim[setor['id']][i] = matriz_soma_de_sim[setor['id']][i] + 1
                                if resposta['resposta'] == "nao":
                                    matriz_soma_de_nao[setor['id']][i] = matriz_soma_de_nao[setor['id']][i] + 1
                                if resposta['resposta'] == "na":
                                    matriz_soma_de_nao_se_aplica[setor['id']][i] = matriz_soma_de_nao_se_aplica[setor['id']][i] + 1

        for i in range(1,quantidade_de_setores+1):
            for j in range(1,quantidade_de_dimensoes+1):
                matriz_soma_de_sim[0][j] = matriz_soma_de_sim[0][j] + matriz_soma_de_sim[i][j]
                matriz_soma_de_nao[0][j] = matriz_soma_de_nao[0][j] + matriz_soma_de_nao[i][j]
                matriz_soma_de_nao_se_aplica[0][j] = matriz_soma_de_nao_se_aplica[0][j] + matriz_soma_de_nao_se_aplica[i][j]

        for i in range(0,quantidade_de_setores+1):
            for j in range(0,quantidade_de_dimensoes+1):
                matriz_soma_de_sim[i][0] = matriz_soma_de_sim[i][0] + matriz_soma_de_sim[i][j]
                matriz_soma_de_nao[i][0] = matriz_soma_de_nao[i][0] + matriz_soma_de_nao[i][j]
                matriz_soma_de_nao_se_aplica[i][0] = matriz_soma_de_nao_se_aplica[i][0] + matriz_soma_de_nao_se_aplica[i][j]

        for i in range(0,quantidade_de_setores+1):
            for j in range(0,quantidade_de_dimensoes+1):
                if matriz_soma_de_sim[i][j]+matriz_soma_de_nao[i][j] != 0:
                    matriz_de_porcentagens_sim[i][j] = round((matriz_soma_de_sim[i][j]/(matriz_soma_de_sim[i][j]+matriz_soma_de_nao[i][j]))*100, 2) 
                    matriz_de_porcentagens_nao[i][j] = round((matriz_soma_de_nao[i][j]/(matriz_soma_de_sim[i][j]+matriz_soma_de_nao[i][j]))*100, 2)
        print(lista_de_dimensoes_distintas)
        pprint.pprint(matriz_de_dimensoes)
        pprint.pprint(matriz_de_id_dimensoes)
        pprint.pprint(meses_distintos_de_respostas)
        
        lista_soma_de_sim_filtrada_por_setor_escolhido = []
        lista_soma_de_nao_filtrada_por_setor_escolhido = []
        lista_soma_de_nao_se_aplica_filtrada_por_setor_escolhido = []
        lista_de_porcentagens_de_sim_filtrada_por_setor_escolhido = []
        for setor in range(0,quantidade_de_setores+1):
            if setor == int(setor_escolhido):
                for dimensao in range(0,quantidade_de_dimensoes+1):
                    lista_soma_de_sim_filtrada_por_setor_escolhido.append(matriz_soma_de_sim[setor][dimensao])
                    lista_soma_de_nao_filtrada_por_setor_escolhido.append(matriz_soma_de_nao[setor][dimensao])
                    lista_soma_de_nao_se_aplica_filtrada_por_setor_escolhido.append(matriz_soma_de_nao_se_aplica[setor][dimensao])
                    lista_de_porcentagens_de_sim_filtrada_por_setor_escolhido.append(matriz_de_porcentagens_sim[setor][dimensao])
        
        context ={
            'bloq_tela':request.session.get('id_setor'),
            'nm_colaborador':request.session.get('nm_colaborador'),
            'escolha_setor':setor_escolhido,
            'nome_do_setor_escolhido':nome_do_setor_escolhido,
            'data_inicial_escolhida':string_da_data_inicial_escolhida,
            'data_final_escolhida':string_da_data_final_escolhida,
            'matriz_de_dimensoes':matriz_de_dimensoes,
            'matriz_de_porcentagens_sim':matriz_de_porcentagens_sim,
            'lista_de_porcentagens_de_sim_filtrada_por_setor_escolhido':lista_de_porcentagens_de_sim_filtrada_por_setor_escolhido,
            'matriz_de_porcentagens_nao':matriz_de_porcentagens_nao,
            'matriz_soma_de_sim':matriz_soma_de_sim,
            'lista_soma_de_sim_filtrada_por_setor_escolhido':lista_soma_de_sim_filtrada_por_setor_escolhido,
            'matriz_soma_de_nao':matriz_soma_de_nao,
            'lista_soma_de_nao_filtrada_por_setor_escolhido':lista_soma_de_nao_filtrada_por_setor_escolhido,
            'matriz_soma_de_nao_se_aplica':matriz_soma_de_nao_se_aplica,
            'lista_soma_de_nao_se_aplica_filtrada_por_setor_escolhido':lista_soma_de_nao_se_aplica_filtrada_por_setor_escolhido,
            'setores':data_setor,
            'respostas':data_resposta,
            'matriz_de_porcentagens_sim_por_mes_assistencial':matriz_de_porcentagens_sim_por_mes_assistencial,
            'matriz_de_porcentagens_sim_por_mes_documentos':matriz_de_porcentagens_sim_por_mes_documentos,
            'matriz_de_porcentagens_sim_por_mes_estoque':matriz_de_porcentagens_sim_por_mes_estoque,
            'matriz_de_porcentagens_sim_por_mes_hotelaria':matriz_de_porcentagens_sim_por_mes_hotelaria,
            'matriz_de_porcentagens_sim_por_mes_manutencao':matriz_de_porcentagens_sim_por_mes_manutencao,
            'matriz_de_porcentagens_sim_por_mes_pessoas':matriz_de_porcentagens_sim_por_mes_pessoas,
            'meses_distintos_de_resposta':meses_distintos_de_respostas,
        }
        return render(request, 'scoreboard-relatorio.html', context)

    url_setor =  f'http://{host}/setores/'

    response_setor = requests.get(url=url_setor, headers=headers)

    data_setor = response_setor.json()

    context ={
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'setores':data_setor
    }
    return render(request, 'filtro-para-dashboard.html', context)

def dashboardProctorFiltroPorSetor(request):
    global setor_escolhido
    global data_inicial_escolhida
    global data_final_escolhida

    global matriz_soma_de_sim
    global matriz_soma_de_nao
    global matriz_soma_de_nao_se_aplica
    global matriz_de_porcentagens_sim
    global matriz_de_porcentagens_nao
    global meses_distintos_de_respostas


    global matriz_soma_de_sim_por_mes_assistencial
    global matriz_soma_de_nao_por_mes_assistencial
    global matriz_de_porcentagens_sim_por_mes_assistencial

    global matriz_soma_de_sim_por_mes_documentos
    global matriz_soma_de_nao_por_mes_documentos
    global matriz_de_porcentagens_sim_por_mes_documentos

    global matriz_soma_de_sim_por_mes_estoque
    global matriz_soma_de_nao_por_mes_estoque
    global matriz_de_porcentagens_sim_por_mes_estoque

    global matriz_soma_de_sim_por_mes_hotelaria
    global matriz_soma_de_nao_por_mes_hotelaria
    global matriz_de_porcentagens_sim_por_mes_hotelaria

    global matriz_soma_de_sim_por_mes_manutencao
    global matriz_soma_de_nao_por_mes_manutencao
    global matriz_de_porcentagens_sim_por_mes_manutencao

    global matriz_soma_de_sim_por_mes_pessoas
    global matriz_soma_de_nao_por_mes_pessoas
    global matriz_de_porcentagens_sim_por_mes_pessoas

    global matriz_de_dimensoes
    global matriz_de_id_dimensoes
    

    headers = request.session.get('headers')
    if not headers:
        return render(request, 'pages-error-404.html')

    if request.method == "POST":
        setor_escolhido = request.POST.get('setor')
        data_inicial_escolhida = request.POST.get('data_relatorio_inicial')
        data_final_escolhida = request.POST.get('data_relatorio_final')
        
        ano_data_inicial_escolhida = data_inicial_escolhida[0:4]
        mes_data_inicial_escolhida = data_inicial_escolhida[5:7]
        dia_data_inicial_escolhida = data_inicial_escolhida[8:10]
        string_da_data_inicial_escolhida = dia_data_inicial_escolhida + "/"  + mes_data_inicial_escolhida + "/" + ano_data_inicial_escolhida
        numero_da_data_inicial_escolhida = int(ano_data_inicial_escolhida + mes_data_inicial_escolhida + dia_data_inicial_escolhida)

        ano_data_final_escolhida = data_final_escolhida[0:4]
        mes_data_final_escolhida = data_final_escolhida[5:7]
        dia_data_final_escolhida = data_final_escolhida[8:10]
        string_da_data_final_escolhida = dia_data_final_escolhida + "/"  + mes_data_final_escolhida + "/" + ano_data_final_escolhida
        numero_da_data_final_escolhida = int(ano_data_final_escolhida + mes_data_final_escolhida + dia_data_final_escolhida)

        
        url_setor =  f'http://{host}/setores/'
        url_dimensao = f'http://{host}/prontocheck/dimensao/'
        url_resposta_filtro_por_setor_escolhido = f'http://{host}/prontocheck/resposta/?setor={setor_escolhido}'
        url_dimensao_filtro_por_setor_escolhido =  f'http://{host}/prontocheck/dimensao/?setor={setor_escolhido}'
        url_titulo_filtro_por_setor_escolhido =  f'http://{host}/prontocheck/titulo/?setor={setor_escolhido}'
        url_pergunta_filtro_por_setor_escolhido = f'http://{host}/prontocheck/pergunta/?setor={setor_escolhido}'

        response_setor = requests.get(url=url_setor, headers=headers)
        response_dimensao = requests.get(url=url_dimensao, headers=headers)
        response_resposta_filtro_por_setor_escolhido = requests.get(url=url_resposta_filtro_por_setor_escolhido, headers=headers)
        response_dimensao_filtro_por_setor_escolhido = requests.get(url=url_dimensao_filtro_por_setor_escolhido, headers=headers)
        response_titulo_filtro_por_setor_escolhido = requests.get(url=url_titulo_filtro_por_setor_escolhido, headers=headers)
        response_pergunta_filtro_por_setor_escolhido = requests.get(url=url_pergunta_filtro_por_setor_escolhido, headers=headers)

        data_setor = response_setor.json()
        data_dimensao = response_dimensao.json()
        data_resposta_filtro_por_setor_escolhido = response_resposta_filtro_por_setor_escolhido.json()
        data_dimensao_filtro_por_setor_escolhido = response_dimensao_filtro_por_setor_escolhido.json()
        data_titulo_filtro_por_setor_escolhido = response_titulo_filtro_por_setor_escolhido.json()
        data_pergunta_filtro_por_setor_escolhido = response_pergunta_filtro_por_setor_escolhido.json()

        matriz_soma_de_sim = []
        matriz_soma_de_nao = []
        matriz_soma_de_nao_se_aplica = []
        matriz_de_porcentagens_sim = []
        matriz_de_porcentagens_nao = []
        meses_distintos_de_respostas = []

        matriz_soma_de_sim_por_mes_assistencial = []
        matriz_soma_de_nao_por_mes_assistencial = []
        matriz_de_porcentagens_sim_por_mes_assistencial = []

        matriz_soma_de_sim_por_mes_documentos = []
        matriz_soma_de_nao_por_mes_documentos = []
        matriz_de_porcentagens_sim_por_mes_documentos = []

        matriz_soma_de_sim_por_mes_estoque = []
        matriz_soma_de_nao_por_mes_estoque = []
        matriz_de_porcentagens_sim_por_mes_estoque = []

        matriz_soma_de_sim_por_mes_hotelaria = []
        matriz_soma_de_nao_por_mes_hotelaria = []
        matriz_de_porcentagens_sim_por_mes_hotelaria = []

        matriz_soma_de_sim_por_mes_manutencao = []
        matriz_soma_de_nao_por_mes_manutencao = []
        matriz_de_porcentagens_sim_por_mes_manutencao = []

        matriz_soma_de_sim_por_mes_pessoas = []
        matriz_soma_de_nao_por_mes_pessoas = []
        matriz_de_porcentagens_sim_por_mes_pessoas = []

        matriz_de_dimensoes = []
        matriz_de_id_dimensoes = []
        
        for setor in data_setor:
            if setor['id'] == int(setor_escolhido):
                nome_do_setor_escolhido = setor['name']

        dimensoes = []
        lista_de_dimensoes_distintas = []
        for dimensao in data_dimensao:
            dimensoes.append(dimensao['dimensao'])
        dimensoes = set(dimensoes)

        for dimensao in dimensoes:
            lista_de_dimensoes_distintas.append(dimensao)

        quantidade_de_setores = len(data_setor)
        quantidade_de_dimensoes = len(lista_de_dimensoes_distintas)

        matriz_de_id_dimensoes = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_sim = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_se_aplica = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_dimensoes = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_nao = [[0 for _ in range(quantidade_de_dimensoes+1)] for _ in range(quantidade_de_setores+1)]
 
        meses_de_respostas = []
        ano_de_respostas = []
        for resposta in data_resposta_filtro_por_setor_escolhido:
            mes_da_resposta = resposta['created_at']
            mes_da_resposta = mes_da_resposta[0:7]
            ano_da_resposta = mes_da_resposta[0:4]
            ano_de_respostas.append(ano_da_resposta)
            meses_de_respostas.append(mes_da_resposta)

        meses_de_respostas = set(meses_de_respostas)
        ano_de_respostas = set(ano_de_respostas)
        quantidade_de_anos = len(ano_de_respostas)
        quantidade_de_meses = quantidade_de_anos*12

        for mes in meses_de_respostas:
            meses_distintos_de_respostas.append(mes)
        
        meses_distintos_de_respostas = sorted(meses_distintos_de_respostas)
        quantidade_de_meses_preenchidos = len(meses_distintos_de_respostas)
        
        todos_os_meses_do_ano = []
        for ano in ano_de_respostas:
            mes = 1
            for _ in range(12):
                if (len(str(mes))==1):
                    mes_e_ano = ano + "-" + "0" + str(mes)
                else:
                    mes_e_ano = ano + "-" + str(mes)
                todos_os_meses_do_ano.append(mes_e_ano)
                mes = mes + 1
        

        matriz_soma_de_sim_por_mes_assistencial = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_por_mes_assistencial = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim_por_mes_assistencial = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]

        matriz_soma_de_sim_por_mes_documentos = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_por_mes_documentos = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim_por_mes_documentos = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]

        matriz_soma_de_sim_por_mes_estoque = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_por_mes_estoque = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim_por_mes_estoque = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]

        matriz_soma_de_sim_por_mes_hotelaria = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_por_mes_hotelaria = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim_por_mes_hotelaria = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)] 

        matriz_soma_de_sim_por_mes_manutencao = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_por_mes_manutencao = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim_por_mes_manutencao = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]

        matriz_soma_de_sim_por_mes_pessoas = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_soma_de_nao_por_mes_pessoas = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        matriz_de_porcentagens_sim_por_mes_pessoas = [[0 for _ in range(quantidade_de_meses+1)] for _ in range(quantidade_de_setores+1)]
        
        for dimensao in data_dimensao_filtro_por_setor_escolhido:
            if dimensao['dimensao'] == 'DIMENSÃO ASSISTENCIAL':
                matriz_soma_de_sim_por_mes_assistencial[int(setor_escolhido)][0] = dimensao['id']
                matriz_soma_de_nao_por_mes_assistencial[int(setor_escolhido)][0] = dimensao['id']                        
                matriz_de_porcentagens_sim_por_mes_assistencial[int(setor_escolhido)][0] = dimensao['id']
            if dimensao['dimensao'] == 'DIMENSÃO DOCUMENTOS':
                matriz_soma_de_sim_por_mes_documentos[int(setor_escolhido)][0] = dimensao['id']
                matriz_soma_de_nao_por_mes_documentos[int(setor_escolhido)][0] = dimensao['id']                        
                matriz_de_porcentagens_sim_por_mes_documentos[int(setor_escolhido)][0] = dimensao['id']
            if dimensao['dimensao'] == 'DIMENSÃO ESTOQUE':
                matriz_soma_de_sim_por_mes_estoque[int(setor_escolhido)][0] = dimensao['id']
                matriz_soma_de_nao_por_mes_estoque[int(setor_escolhido)][0] = dimensao['id']                        
                matriz_de_porcentagens_sim_por_mes_estoque[int(setor_escolhido)][0] = dimensao['id']
            if dimensao['dimensao'] == 'DIMENSÃO HOTELARIA':
                matriz_soma_de_sim_por_mes_hotelaria[int(setor_escolhido)][0] = dimensao['id']
                matriz_soma_de_nao_por_mes_hotelaria[int(setor_escolhido)][0] = dimensao['id']                        
                matriz_de_porcentagens_sim_por_mes_hotelaria[int(setor_escolhido)][0] = dimensao['id']
            if dimensao['dimensao'] == 'DIMENSÃO MANUTENÇÃO':
                matriz_soma_de_sim_por_mes_manutencao[int(setor_escolhido)][0] = dimensao['id']
                matriz_soma_de_nao_por_mes_manutencao[int(setor_escolhido)][0] = dimensao['id']                        
                matriz_de_porcentagens_sim_por_mes_manutencao[int(setor_escolhido)][0] = dimensao['id']
            if dimensao['dimensao'] == 'DIMENSÃO PESSOAS':
                matriz_soma_de_sim_por_mes_pessoas[int(setor_escolhido)][0] = dimensao['id']
                matriz_soma_de_nao_por_mes_pessoas[int(setor_escolhido)][0] = dimensao['id']                        
                matriz_de_porcentagens_sim_por_mes_pessoas[int(setor_escolhido)][0] = dimensao['id']

        for resposta in data_resposta_filtro_por_setor_escolhido:
            for i in range(0,len(todos_os_meses_do_ano)):
                mes_da_resposta = resposta['created_at']
                mes_da_resposta = mes_da_resposta[0:7]
                if todos_os_meses_do_ano[i] == mes_da_resposta:
                    if resposta['dimensao'] == matriz_soma_de_sim_por_mes_assistencial[int(setor_escolhido)][0]:
                        if resposta['resposta'] == "sim":
                            matriz_soma_de_sim_por_mes_assistencial[int(setor_escolhido)][i+1] = matriz_soma_de_sim_por_mes_assistencial[int(setor_escolhido)][i+1] + 1
                        if resposta['resposta'] == "nao":
                            matriz_soma_de_nao_por_mes_assistencial[int(setor_escolhido)][i+1] = matriz_soma_de_nao_por_mes_assistencial[int(setor_escolhido)][i+1] + 1
                    if resposta['dimensao'] == matriz_soma_de_sim_por_mes_documentos[int(setor_escolhido)][0]:
                        if resposta['resposta'] == "sim":
                            matriz_soma_de_sim_por_mes_documentos[int(setor_escolhido)][i+1] = matriz_soma_de_sim_por_mes_documentos[int(setor_escolhido)][i+1] + 1
                        if resposta['resposta'] == "nao":
                            matriz_soma_de_nao_por_mes_documentos[int(setor_escolhido)][i+1] = matriz_soma_de_nao_por_mes_documentos[int(setor_escolhido)][i+1] + 1
                    if resposta['dimensao'] == matriz_soma_de_sim_por_mes_estoque[int(setor_escolhido)][0]:
                        if resposta['resposta'] == "sim":
                            matriz_soma_de_sim_por_mes_estoque[int(setor_escolhido)][i+1] = matriz_soma_de_sim_por_mes_estoque[int(setor_escolhido)][i+1] + 1
                        if resposta['resposta'] == "nao":
                            matriz_soma_de_nao_por_mes_estoque[int(setor_escolhido)][i+1] = matriz_soma_de_nao_por_mes_estoque[int(setor_escolhido)][i+1] + 1
                    if resposta['dimensao'] == matriz_soma_de_sim_por_mes_hotelaria[int(setor_escolhido)][0]:
                        if resposta['resposta'] == "sim":
                            matriz_soma_de_sim_por_mes_hotelaria[int(setor_escolhido)][i+1] = matriz_soma_de_sim_por_mes_hotelaria[int(setor_escolhido)][i+1] + 1
                        if resposta['resposta'] == "nao":
                            matriz_soma_de_nao_por_mes_hotelaria[int(setor_escolhido)][i+1] = matriz_soma_de_nao_por_mes_hotelaria[int(setor_escolhido)][i+1] + 1
                    if resposta['dimensao'] == matriz_soma_de_sim_por_mes_manutencao[int(setor_escolhido)][0]:
                        if resposta['resposta'] == "sim":
                            matriz_soma_de_sim_por_mes_manutencao[int(setor_escolhido)][i+1] = matriz_soma_de_sim_por_mes_manutencao[int(setor_escolhido)][i+1] + 1
                        if resposta['resposta'] == "nao":
                            matriz_soma_de_nao_por_mes_manutencao[int(setor_escolhido)][i+1] = matriz_soma_de_nao_por_mes_manutencao[int(setor_escolhido)][i+1] + 1
                    if resposta['dimensao'] == matriz_soma_de_sim_por_mes_pessoas[int(setor_escolhido)][0]:
                        if resposta['resposta'] == "sim":
                            matriz_soma_de_sim_por_mes_pessoas[int(setor_escolhido)][i+1] = matriz_soma_de_sim_por_mes_pessoas[int(setor_escolhido)][i+1] + 1
                        if resposta['resposta'] == "nao":
                            matriz_soma_de_nao_por_mes_pessoas[int(setor_escolhido)][i+1] = matriz_soma_de_nao_por_mes_pessoas[int(setor_escolhido)][i+1] + 1

        for i in range(0,quantidade_de_setores+1):
            for j in range(1,len(todos_os_meses_do_ano)+1):
                if matriz_soma_de_sim_por_mes_assistencial[i][j]+matriz_soma_de_nao_por_mes_assistencial[i][j] != 0:
                    matriz_de_porcentagens_sim_por_mes_assistencial[i][j] = round((matriz_soma_de_sim_por_mes_assistencial[i][j]/(matriz_soma_de_sim_por_mes_assistencial[i][j]+matriz_soma_de_nao_por_mes_assistencial[i][j]))*100, 2) 
                if matriz_soma_de_sim_por_mes_documentos[i][j]+matriz_soma_de_nao_por_mes_documentos[i][j] != 0:
                    matriz_de_porcentagens_sim_por_mes_documentos[i][j] = round((matriz_soma_de_sim_por_mes_documentos[i][j]/(matriz_soma_de_sim_por_mes_documentos[i][j]+matriz_soma_de_nao_por_mes_documentos[i][j]))*100, 2) 
                if matriz_soma_de_sim_por_mes_estoque[i][j]+matriz_soma_de_nao_por_mes_estoque[i][j] != 0:
                    matriz_de_porcentagens_sim_por_mes_estoque[i][j] = round((matriz_soma_de_sim_por_mes_estoque[i][j]/(matriz_soma_de_sim_por_mes_estoque[i][j]+matriz_soma_de_nao_por_mes_estoque[i][j]))*100, 2) 
                if matriz_soma_de_sim_por_mes_hotelaria[i][j]+matriz_soma_de_nao_por_mes_hotelaria[i][j] != 0:
                    matriz_de_porcentagens_sim_por_mes_hotelaria[i][j] = round((matriz_soma_de_sim_por_mes_hotelaria[i][j]/(matriz_soma_de_sim_por_mes_hotelaria[i][j]+matriz_soma_de_nao_por_mes_hotelaria[i][j]))*100, 2) 
                if matriz_soma_de_sim_por_mes_manutencao[i][j]+matriz_soma_de_nao_por_mes_manutencao[i][j] != 0:
                    matriz_de_porcentagens_sim_por_mes_manutencao[i][j] = round((matriz_soma_de_sim_por_mes_manutencao[i][j]/(matriz_soma_de_sim_por_mes_manutencao[i][j]+matriz_soma_de_nao_por_mes_manutencao[i][j]))*100, 2) 
                if matriz_soma_de_sim_por_mes_pessoas[i][j]+matriz_soma_de_nao_por_mes_pessoas[i][j] != 0:                    
                    matriz_de_porcentagens_sim_por_mes_pessoas[i][j] = round((matriz_soma_de_sim_por_mes_pessoas[i][j]/(matriz_soma_de_sim_por_mes_pessoas[i][j]+matriz_soma_de_nao_por_mes_pessoas[i][j]))*100, 2) 

        lista_de_porcentagens_sim_por_mes_assistencial_filtrada_por_setor_escolhido = []
        lista_de_porcentagens_sim_por_mes_documentos_filtrada_por_setor_escolhido = []
        lista_de_porcentagens_sim_por_mes_estoque_filtrada_por_setor_escolhido = []
        lista_de_porcentagens_sim_por_mes_hotelaria_filtrada_por_setor_escolhido = []
        lista_de_porcentagens_sim_por_mes_manutencao_filtrada_por_setor_escolhido = []
        lista_de_porcentagens_sim_por_mes_pessoas_filtrada_por_setor_escolhido = []
        for setor in range(0,quantidade_de_setores+1):
            if setor == int(setor_escolhido):
                for mes in range(0,len(todos_os_meses_do_ano)+1):
                    lista_de_porcentagens_sim_por_mes_assistencial_filtrada_por_setor_escolhido.append(matriz_de_porcentagens_sim_por_mes_assistencial[setor][mes])
                    lista_de_porcentagens_sim_por_mes_documentos_filtrada_por_setor_escolhido.append(matriz_de_porcentagens_sim_por_mes_documentos[setor][mes])
                    lista_de_porcentagens_sim_por_mes_estoque_filtrada_por_setor_escolhido.append(matriz_de_porcentagens_sim_por_mes_estoque[setor][mes])
                    lista_de_porcentagens_sim_por_mes_hotelaria_filtrada_por_setor_escolhido.append(matriz_de_porcentagens_sim_por_mes_hotelaria[setor][mes])
                    lista_de_porcentagens_sim_por_mes_manutencao_filtrada_por_setor_escolhido.append(matriz_de_porcentagens_sim_por_mes_manutencao[setor][mes])
                    lista_de_porcentagens_sim_por_mes_pessoas_filtrada_por_setor_escolhido.append(matriz_de_porcentagens_sim_por_mes_pessoas[setor][mes])
        lista_de_porcentagens_sim_por_mes_assistencial_filtrada_por_setor_escolhido.remove(lista_de_porcentagens_sim_por_mes_assistencial_filtrada_por_setor_escolhido[0])
        lista_de_porcentagens_sim_por_mes_documentos_filtrada_por_setor_escolhido.remove(lista_de_porcentagens_sim_por_mes_documentos_filtrada_por_setor_escolhido[0])
        lista_de_porcentagens_sim_por_mes_estoque_filtrada_por_setor_escolhido.remove(lista_de_porcentagens_sim_por_mes_estoque_filtrada_por_setor_escolhido[0])
        lista_de_porcentagens_sim_por_mes_hotelaria_filtrada_por_setor_escolhido.remove(lista_de_porcentagens_sim_por_mes_hotelaria_filtrada_por_setor_escolhido[0])
        lista_de_porcentagens_sim_por_mes_manutencao_filtrada_por_setor_escolhido.remove(lista_de_porcentagens_sim_por_mes_manutencao_filtrada_por_setor_escolhido[0])
        lista_de_porcentagens_sim_por_mes_pessoas_filtrada_por_setor_escolhido.remove(lista_de_porcentagens_sim_por_mes_pessoas_filtrada_por_setor_escolhido[0])
        for resposta in data_resposta_filtro_por_setor_escolhido:
            dataAbertura = resposta['created_at']
            dataAbertura = dataAbertura[0:10]
            resposta['created_at'] = dataAbertura
        
        for dimensao in data_dimensao_filtro_por_setor_escolhido:
            if dimensao['dimensao'] == 'DIMENSÃO ASSISTENCIAL':
                matriz_de_dimensoes[int(setor_escolhido)][1] = 'DIMENSÃO ASSISTENCIAL'
                matriz_de_id_dimensoes[int(setor_escolhido)][1] = dimensao['id']
            if dimensao['dimensao'] == 'DIMENSÃO DOCUMENTOS':
                matriz_de_dimensoes[int(setor_escolhido)][2] = 'DIMENSÃO DOCUMENTOS'
                matriz_de_id_dimensoes[int(setor_escolhido)][2] = dimensao['id']
            if dimensao['dimensao'] == 'DIMENSÃO ESTOQUE':
                matriz_de_dimensoes[int(setor_escolhido)][3] = 'DIMENSÃO ESTOQUE'
                matriz_de_id_dimensoes[int(setor_escolhido)][3] = dimensao['id']
            if dimensao['dimensao'] == 'DIMENSÃO HOTELARIA':
                matriz_de_dimensoes[int(setor_escolhido)][4] = 'DIMENSÃO HOTELARIA'
                matriz_de_id_dimensoes[int(setor_escolhido)][4] = dimensao['id']
            if dimensao['dimensao'] == 'DIMENSÃO MANUTENÇÃO':
                matriz_de_dimensoes[int(setor_escolhido)][5] = 'DIMENSÃO MANUTENÇÃO'
                matriz_de_id_dimensoes[int(setor_escolhido)][5] = dimensao['id']
            if dimensao['dimensao'] == 'DIMENSÃO PESSOAS':
                matriz_de_dimensoes[int(setor_escolhido)][6] = 'DIMENSÃO PESSOAS'
                matriz_de_id_dimensoes[int(setor_escolhido)][6] = dimensao['id']

        for resposta in data_resposta_filtro_por_setor_escolhido:
            ano_resposta = resposta['created_at'][0:4]
            mes_resposta = resposta['created_at'][5:7]
            dia_resposta = resposta['created_at'][8:10]
            numero_da_data_resposta = int(ano_resposta + mes_resposta + dia_resposta)
            if numero_da_data_inicial_escolhida <= numero_da_data_resposta and numero_da_data_resposta <= numero_da_data_final_escolhida:
                for i in range(0,quantidade_de_dimensoes+1):
                    if matriz_de_id_dimensoes[int(setor_escolhido)][i] == resposta['dimensao']:
                        if resposta['resposta'] == "sim":
                            matriz_soma_de_sim[int(setor_escolhido)][i] = matriz_soma_de_sim[int(setor_escolhido)][i] + 1
                        if resposta['resposta'] == "nao":
                            matriz_soma_de_nao[int(setor_escolhido)][i] = matriz_soma_de_nao[int(setor_escolhido)][i] + 1
                        if resposta['resposta'] == "na":
                            matriz_soma_de_nao_se_aplica[int(setor_escolhido)][i] = matriz_soma_de_nao_se_aplica[int(setor_escolhido)][i] + 1

        data_resposta_filtro_por_setor_e_por_periodo_escolhido = []
        for resposta in data_resposta_filtro_por_setor_escolhido:
            ano_resposta = resposta['created_at'][0:4]
            mes_resposta = resposta['created_at'][5:7]
            dia_resposta = resposta['created_at'][8:10]
            numero_da_data_resposta = int(ano_resposta + mes_resposta + dia_resposta)
            if numero_da_data_inicial_escolhida <= numero_da_data_resposta and numero_da_data_resposta <= numero_da_data_final_escolhida:
                data_resposta_filtro_por_setor_e_por_periodo_escolhido.append(resposta)
                for dimensao in data_dimensao_filtro_por_setor_escolhido:
                    for titulo in data_titulo_filtro_por_setor_escolhido:
                        for pergunta in data_pergunta_filtro_por_setor_escolhido:
                            if resposta['dimensao'] == dimensao['id']:
                                resposta['dimensao'] = dimensao['dimensao']
                            if resposta['titulo'] == titulo['id']:
                                resposta['titulo'] = titulo['titulo']
                            if resposta['pergunta'] == pergunta['id']:
                                resposta['pergunta'] = pergunta['pergunta']
                            
        for i in range(1,quantidade_de_setores+1):
            for j in range(1,quantidade_de_dimensoes+1):
                matriz_soma_de_sim[0][j] = matriz_soma_de_sim[0][j] + matriz_soma_de_sim[i][j]
                matriz_soma_de_nao[0][j] = matriz_soma_de_nao[0][j] + matriz_soma_de_nao[i][j]
                matriz_soma_de_nao_se_aplica[0][j] = matriz_soma_de_nao_se_aplica[0][j] + matriz_soma_de_nao_se_aplica[i][j]

        for i in range(0,quantidade_de_setores+1):
            for j in range(0,quantidade_de_dimensoes+1):
                matriz_soma_de_sim[i][0] = matriz_soma_de_sim[i][0] + matriz_soma_de_sim[i][j]
                matriz_soma_de_nao[i][0] = matriz_soma_de_nao[i][0] + matriz_soma_de_nao[i][j]
                matriz_soma_de_nao_se_aplica[i][0] = matriz_soma_de_nao_se_aplica[i][0] + matriz_soma_de_nao_se_aplica[i][j]

        for i in range(0,quantidade_de_setores+1):
            for j in range(0,quantidade_de_dimensoes+1):
                if matriz_soma_de_sim[i][j]+matriz_soma_de_nao[i][j] != 0:
                    matriz_de_porcentagens_sim[i][j] = round((matriz_soma_de_sim[i][j]/(matriz_soma_de_sim[i][j]+matriz_soma_de_nao[i][j]))*100, 2) 
                    matriz_de_porcentagens_nao[i][j] = round((matriz_soma_de_nao[i][j]/(matriz_soma_de_sim[i][j]+matriz_soma_de_nao[i][j]))*100, 2)
        
        lista_soma_de_sim_filtrada_por_setor_escolhido = []
        lista_soma_de_nao_filtrada_por_setor_escolhido = []
        lista_soma_de_nao_se_aplica_filtrada_por_setor_escolhido = []
        lista_de_porcentagens_de_sim_filtrada_por_setor_escolhido = []
        for setor in range(0,quantidade_de_setores+1):
            if setor == int(setor_escolhido):
                for dimensao in range(0,quantidade_de_dimensoes+1):
                    lista_soma_de_sim_filtrada_por_setor_escolhido.append(matriz_soma_de_sim[setor][dimensao])
                    lista_soma_de_nao_filtrada_por_setor_escolhido.append(matriz_soma_de_nao[setor][dimensao])
                    lista_soma_de_nao_se_aplica_filtrada_por_setor_escolhido.append(matriz_soma_de_nao_se_aplica[setor][dimensao])
                    lista_de_porcentagens_de_sim_filtrada_por_setor_escolhido.append(matriz_de_porcentagens_sim[setor][dimensao])
        
        context ={
            'bloq_tela':request.session.get('id_setor'),
            'nm_colaborador':request.session.get('nm_colaborador'),
            'escolha_setor':setor_escolhido,
            'nome_do_setor_escolhido':nome_do_setor_escolhido,
            'data_inicial_escolhida':string_da_data_inicial_escolhida,
            'data_final_escolhida':string_da_data_final_escolhida,
            'matriz_de_dimensoes':matriz_de_dimensoes,
            'matriz_de_porcentagens_sim':matriz_de_porcentagens_sim,
            'lista_de_porcentagens_de_sim_filtrada_por_setor_escolhido':lista_de_porcentagens_de_sim_filtrada_por_setor_escolhido,
            'matriz_de_porcentagens_nao':matriz_de_porcentagens_nao,
            'matriz_soma_de_sim':matriz_soma_de_sim,
            'lista_soma_de_sim_filtrada_por_setor_escolhido':lista_soma_de_sim_filtrada_por_setor_escolhido,
            'matriz_soma_de_nao':matriz_soma_de_nao,
            'lista_soma_de_nao_filtrada_por_setor_escolhido':lista_soma_de_nao_filtrada_por_setor_escolhido,
            'matriz_soma_de_nao_se_aplica':matriz_soma_de_nao_se_aplica,
            'lista_soma_de_nao_se_aplica_filtrada_por_setor_escolhido':lista_soma_de_nao_se_aplica_filtrada_por_setor_escolhido,
            'setores':data_setor,
            'respostas':data_resposta_filtro_por_setor_e_por_periodo_escolhido,
            'lista_de_porcentagens_sim_por_mes_assistencial_filtrada_por_setor_escolhido':lista_de_porcentagens_sim_por_mes_assistencial_filtrada_por_setor_escolhido,
            'lista_de_porcentagens_sim_por_mes_documentos_filtrada_por_setor_escolhido':lista_de_porcentagens_sim_por_mes_documentos_filtrada_por_setor_escolhido,
            'lista_de_porcentagens_sim_por_mes_estoque_filtrada_por_setor_escolhido':lista_de_porcentagens_sim_por_mes_estoque_filtrada_por_setor_escolhido,
            'lista_de_porcentagens_sim_por_mes_hotelaria_filtrada_por_setor_escolhido':lista_de_porcentagens_sim_por_mes_hotelaria_filtrada_por_setor_escolhido,
            'lista_de_porcentagens_sim_por_mes_manutencao_filtrada_por_setor_escolhido':lista_de_porcentagens_sim_por_mes_manutencao_filtrada_por_setor_escolhido,
            'lista_de_porcentagens_sim_por_mes_pessoas_filtrada_por_setor_escolhido':lista_de_porcentagens_sim_por_mes_pessoas_filtrada_por_setor_escolhido,
            'meses_distintos_de_resposta':meses_distintos_de_respostas,
            'todos_os_meses_do_ano':todos_os_meses_do_ano,
        }
        return render(request, 'scoreboard-relatorio.html', context)

    url_setor =  f'http://{host}/setores/'

    response_setor = requests.get(url=url_setor, headers=headers)

    data_setor = response_setor.json()
    context ={
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'setores':data_setor
    }
    return render(request, 'filtro-para-dashboard.html', context)

#--------Inicia avaliação-----#

def escolheSetor(request):
    global setor_av_id
    global setor_r
    global armazena_nome_S
    global setor_av_id

    headers = request.session.get('headers')
    if not headers:
        return render(request, 'pages-error-404.html')

    urlset =  f'http://{host}/prontocheck/setor/'
    response = requests.get(url=urlset, headers=headers)
    data = response.json()

    if request.method == "POST":
        request.session['id_setor_aval'] = request.POST.get('setor_av_id')
        var1 = request.session.get('id_setor_aval')
        print(f'O setor é{var1}')
        return redirect('/prontocardio/prontocheck/avaliacao/')

    context = {
        'setores_c': data,
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    } 
       
    return render(request, 'escolheSetor.html', context)

def avaliacao(request):
    #Autenticação de login 
    global setor_r
    global armazena_nome_S
    

    headers = request.session.get('headers')
    if not headers:
        return render(request, 'pages-error-404.html')

    urlset =  f'http://{host}/prontocheck/setor/'
    response = requests.get(url=urlset, headers=headers)
    data = response.json()

    urldim =  f'http://{host}/prontocheck/dimensao/'
    responseDimensao = requests.get(url=urldim, headers=headers)
    dataDim = responseDimensao.json()

    var1 = request.session.get('id_setor_aval')
    print(f'O setor é{var1}')

    if request.method == 'POST':
        ab = request.session.get('id_setor_aval')
        cd = request.POST.get('dimen_av_id')
        return redirect(f'/prontocardio/prontocheck/iniciar_avaliacao/{cd}/{ab}')

    context = {
        'dimen_c': dataDim,
        'setor_av_id': int(request.session.get('id_setor_aval')),
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    return render(request, 'iniciar-avaliacao.html', context)

def iniciarAval(request,id_dim, id_set):
    #Autenticação de login 
    headers = request.session.get('headers')
    n_usu = request.session.get('nm_colaborador')
    id_usu = request.session.get('id_usuario') 
    if not headers:
        return render(request, 'pages-error-404.html')

    data_atual = date.today()
    data_em_texto = data_atual.strftime('%d/%m/%Y')
    print(data_em_texto)
    urlresp = f'http://{host}/prontocheck/resposta/'
    urldim =  f'http://{host}/prontocheck/dimensao/?id={id_dim}'
    urltitulo =  f'http://{host}/prontocheck/titulo/?setor={id_set}&dimensao={id_dim}'
    urlperg = f'http://{host}/prontocheck/pergunta/?setor={id_set}&dimensao={id_dim}'
    urlset =  f'http://{host}/prontocheck/setor/'

    response = requests.get(url=urlset, headers=headers)
    response2 = requests.get(url=urlresp, headers=headers)
    responseDimensao = requests.get(url=urldim, headers=headers)
    response4 = requests.get(url=urltitulo, headers=headers)
    responsePergunta = requests.get(url=urlperg, headers=headers)

    data = response.json()
    data2 = response2.json()
    data4 = response4.json()
    dataPergunta = responsePergunta.json()
    dataDim = responseDimensao.json()
    pprint.pprint(dataDim[0])
    if request.method == "POST":
        print('POST')
        for titulo in data4:
            for pergunta in dataPergunta:
                if pergunta['titulo'] == titulo['id']:
                    pergunta_id  = pergunta["id"]
                    comentario = request.POST.get('comentario{}'.format(pergunta_id))
                    evidencia = request.FILES.get('evidencia{}'.format(pergunta_id))
                    resposta = request.POST.get('pergunta{}'.format(pergunta_id))
                    a_responsavel = request.POST.get('a_resp{}'.format(pergunta_id))
                    print(a_responsavel)
                    data_resp = {
                        "resposta": str(f"{resposta}"),
                        "comentario": str(f"{comentario}"),
                        "setor": int(f"{id_set}"),
                        "dimensao": int(f"{id_dim}"),
                        "titulo": int(f"{titulo['id']}"),
                        "pergunta": int(f"{pergunta_id}"),
                        "user": id_usu,
                    }
                    if a_responsavel is not None:
                        data_resp["a_resp"] = a_responsavel
                    files = {"evidencia": evidencia}
                    responseresp = requests.post(url=urlresp, files=files , data=data_resp, headers=headers)
                    data20  = responseresp.json()
                    print(data20)
                    print(f'A resposta da pergunta #{pergunta["pergunta"]}# é: {resposta}, comentario: {comentario}, evidencia: {evidencia}')
        return redirect('/prontocardio/prontocheck/avaliacao/')
    
    context = {
        'titulos': data4,
        'perguntas': dataPergunta,
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'n_dimensao':dataDim[0],
        'data':data_em_texto,
        'n_usu':n_usu,
        'setorid':id_set,
        'dsetor':data
    }

    return render(request, 'avaliacao.html', context)

#================INDICADORES======================#
def indicadorBI(request):
    context = {
        'bloq_tela':request.session.get('id_setor'),
    }
    return render (request, 'indicadorBI.html', context)
#=============CADASTRO==============================#
def escSetor(request):
    headers = request.session.get('headers')
    if not headers:
        return render(request, 'pages-error-404.html')

    urlset =  f'http://{host}/prontocheck/setor/'
    response = requests.get(url=urlset, headers=headers)
    data = response.json()

    if request.method == "POST":
        setor_av_id = request.POST.get('setor_av_id')
        setor_av_id = int(setor_av_id)
        return redirect(f'/prontocardio/prontocheck/lista_cadastro/{setor_av_id}')

    context = {
        'setores': data,
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    } 
    return render(request, 'setorCad.html', context)

def listaDados(request, idsetor):
    urlDimensao = f'http://{host}/prontocheck/dimensao/'
    urlTitulo = f'http://{host}/prontocheck/titulo/'
    urlPergunta = f'http://{host}/prontocheck/pergunta/'


    headers = request.session.get('headers')
    if not headers:
        return render(request, 'pages-error-404.html')

    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'D':
            dimensao = request.POST['n_dimensao']
            body_dimensao = {
                "dimensao": dimensao,
                "setor": idsetor
            }
            dataDimensao = apiResponse(request,urlDimensao,'POST', data=body_dimensao)
            print(dataDimensao)
            return redirect(request.path)
        elif '_method' in request.POST and request.POST['_method'] == 'T':
            print(urlTitulo)
            dimensao = request.POST['n_dimensao']
            titulo = request.POST['n_titulo']
            body_titulo = {
                "titulo": titulo,
                "dimensao": dimensao,
                "setor":idsetor
            }
            dataTitulo = apiResponse(request,urlTitulo,'POST', data=body_titulo)
            print(dataTitulo)
            return redirect(request.path)
        elif '_method' in request.POST and request.POST['_method'] == 'P':
            pergunta = request.POST['n_pergunta']
            dimensao = request.POST['n_dimensao']
            titulo = request.POST['n_titulo']
            body_pergunta = {
                "pergunta":pergunta,
                "titulo":titulo,
                "dimensao":dimensao,
                "setor": idsetor
            }
            dataPergunta = apiResponse(request,urlPergunta,'POST', data=body_pergunta)
            return redirect(request.path)
        elif '_method' in request.POST and request.POST['_method'] == 'D_ALT':
            body_dimensao = {}
            dimensao = request.POST['n_dimensao']
            id_dim = request.POST['id_Dim']
            peso_dimensao = request.POST['peso_dimensao']
            if dimensao:
                body_dimensao["dimensao"] = dimensao
            if peso_dimensao:
                body_dimensao["peso"] = peso_dimensao                    
            urldimensao = f'http://{host}/prontocheck/dimensao/{id_dim}/'
            responseDimensao = requests.put(url=urldimensao, data=body_dimensao, headers=headers)
            data1 = responseDimensao.json()
            print(data1)
            return redirect(request.path)
        elif '_method' in request.POST and request.POST['_method'] == 'T_ALT':
            id_tit = request.POST['id_titulo']
            dimensao = request.POST['n_dimensao']
            titulo = request.POST['n_titulo']
            body_dimensao = {
                "setor": idsetor
            }
            if dimensao != '':
                body_dimensao["dimensao"] = dimensao

            if titulo != '':
                body_dimensao["titulo"] = titulo
            urldimensao = f'http://{host}/prontocheck/titulo/{id_tit}/'
            responseDimensao = requests.put(url=urldimensao, data=body_dimensao, headers=headers)
            data1 = responseDimensao.json()
            print(data1)
            return redirect(request.path)
        elif '_method' in request.POST and request.POST['_method'] == 'P_ALT':
            id_perg = request.POST['id_pergunta']
            pergunta = request.POST['n_pergunta']
            dimensao = request.POST['n_dimensao']
            titulo = request.POST['n_titulo']
            body_dimensao = {
                "setor": idsetor
            }
            if dimensao != '':
                body_dimensao["dimensao"] = dimensao
            if titulo != '':
                body_dimensao["titulo"] = titulo
            if pergunta != '':
                body_dimensao["pergunta"] = pergunta
            urldimensao = f'http://{host}/prontocheck/pergunta/{id_perg}/'
            responseDimensao = requests.put(url=urldimensao, data=body_dimensao, headers=headers)
            data1 = responseDimensao.json()
            print(data1)
            return redirect(request.path)
        elif '_method' in request.POST and request.POST['_method'] == 'DELETE_DIMENSAO':
            dimensao = request.POST['id_dim']
            url = f'{urlDimensao}{dimensao}/'
            print(url)
            dataDimensao = apiResponse(request,f'{urlDimensao}{dimensao}/','DEL')
            print(dataDimensao)
            return redirect(request.path)
        elif '_method' in request.POST and request.POST['_method'] == 'DELETE_TITULO':
            urlTitulo = f'http://{host}/prontocheck/titulo/'
            titulo = request.POST['id_tit']
            dataTitulo = apiResponse(request,f'{urlTitulo}{titulo}/','DEL')
            print(dataTitulo)
            return redirect(request.path)
        elif '_method' in request.POST and request.POST['_method'] == 'DELETE_PERGUNTA':
            urlPergunta = f'http://{host}/prontocheck/pergunta/'
            pergunta = request.POST['id_pergunta']
            dataPerg = apiResponse(request,f'{urlPergunta}{pergunta}/','DEL')
            print(dataPerg)
            return redirect(request.path)
        else:
            print("else")
    context = {
        'dimensoes':apiResponse(request,f'{urlDimensao}?setor={idsetor}', 'GET' ),
        'titulos':apiResponse(request,f'{urlTitulo}?setor={idsetor}', 'GET' ),
        'perguntas':apiResponse(request,f'{urlPergunta}?setor={idsetor}', 'GET' ),
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'id_setor':idsetor,
        'nm_setor':apiResponse(request,f'{urlSetores}{idsetor}/', 'GET' ),
    } 
    return render(request, 'listaCadastro.html', context)

def verifRel(request, setor):
    #Autenticação de login 
    global setor_r
    global armazena_nome_S
    headers = request.session.get('headers')
    id_usu = request.session.get('id_usuario')
    if not headers:
        return render(request, 'pages-error-404.html')

    setor_r = setor

    urlresp = f'http://{host}/prontocheck/resposta/'
    urldim =  f'http://{host}/prontocheck/dimensao/?setor={setor_r}'
    urltitulo =  f'http://{host}/prontocheck/titulo/?setor={setor_r}'
    urlperg = f'http://{host}/prontocheck/pergunta/?setor={setor_r}'
    urlset =  f'http://{host}/prontocheck/setor/'

    response = requests.get(url=urlset, headers=headers)
    response2 = requests.get(url=urlresp, headers=headers)
    response3 = requests.get(url=urldim, headers=headers)
    response4 = requests.get(url=urltitulo, headers=headers)
    response5 = requests.get(url=urlperg, headers=headers)

    data = response.json()
    data2 = response2.json()
    data3 = response3.json()
    data4 = response4.json()
    data5 = response5.json()

    for item in data2:
        dataAbertura = item['created_at']
        dataAbertura = dataAbertura[0:10]
        item['created_at'] = dataAbertura

    for nome_setor in data:
        if nome_setor['id'] == int(setor_r):
            armazena_nome_S = nome_setor['name']
    
    context = {
        'dimensaos': data3,
        'titulos': data4,
        'perguntas': data5,
        'respostas': data2,
        'setor_esc': int(setor_r),
        'armazena_nome_S': armazena_nome_S,
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'setores': data,
    } 
    return render (request, 'verifRel.html', context)

def teste(request):
    headers = request.session.get('headers')
    if not headers:
        return render(request, 'pages-error-404.html')
    url_resposta = f'http://{host}/prontocheck/resposta/?setor=4'

    response_resposta = requests.get(url=url_resposta, headers=headers)
    
    data_resposta = response_resposta.json()
    data_resposta2 = response_resposta.json()

    meses_distintos_de_respostas = set()
    meses_de_respostas = []

    for resposta in data_resposta:
        item = resposta['created_at']
        data_objeto = datetime.fromisoformat(item)
        data_formatada = data_objeto.strftime("%d/%m/%Y")
        resposta['created_at'] = data_formatada
        mes_da_resposta = resposta['created_at'][:10]
        meses_de_respostas.append(mes_da_resposta)

    meses_distintos_de_respostas = set(meses_de_respostas)


    context = {
        'item':meses_distintos_de_respostas
    }
    return render(request, 'teste.html', context)


def delete_objects(request, objects):
    deleted_ids = []

    for obj in objects:
        print(obj)
        obj_id = obj['id']
        delete_url = f'{urlRespostas}{obj_id}/'
        print(delete_url)

        #response_data = apiResponse(requests, delete_url, 'DEL')
        responsedel = apiResponse(request,delete_url,'DEL')
        print(responsedel)
        if responsedel is not None:
            print(f'Sucesso ao deletar objeto com ID {obj_id}')
            deleted_ids.append(obj_id)
        else:
            print(f'Erro ao deletar objeto com ID {obj_id}: {responsedel}')

    return deleted_ids