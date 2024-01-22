from django.shortcuts import render, redirect
from administrativo.views import apiResponse, host, render_error_404, calcular_diferenca_tempo, obter_data_hora_formatada, calcular_tempo_entre_created_updated
import requests, json, pprint, pytz
from datetime import date
from datetime import datetime
from PIL import Image
from io import BytesIO

urlNaoConformidade = f"http://{host}/notificar/naoconformidade/"
urlStatus = f"http://{host}/notificar/status/"
urlPlanoAcao = f"http://{host}/notificar/planodeacao/"
urlNotificacao = f"http://{host}/notificar/notificacoes/"
urlUsuarios = f"http://{host}/usuarios/"
urlUsuariosV2 = f"http://{host}/usuarios/?funcao=1,2,3,4,5,6"
urlTpIndicador = f"http://{host}/notificar/tpindicadores/"


#=============Sem autenticação==============#
urltpIncidente = f"http://{host}/notificar/tpincidente/"
urlNotificacao_V2 = f"http://{host}/notificar/notificacoes_V2/"
urlSetores = f"http://{host}/notificar/setores/"
#===========================================#
# Retorna a response do determinado endpoint que vai ser acessado
def apiResponseV2(request, urlReceived, requestType, data=None, file=None):
    try:
        if requestType == 'GET':
            response = requests.get(url=urlReceived)
        elif requestType == 'POST':
            response = requests.post(url=urlReceived, data=data, files=file)
            print(response.status_code)
        elif requestType == 'PUT':
            print('Put feito')
            response = requests.put(url=urlReceived, data=data)
            status = response.status_code
        elif requestType == 'DEL':
            print('Função deletar ativada')
            response = requests.delete(url=urlReceived)
            print(response)
        else:
            return None  # Tipo de requisição inválido

        status = response.status_code
        #print(status)
        if 200 <= status < 300:
            try:
                data2 = response.json()
                return data2
            except ValueError:
                return None  # Resposta não é um JSON válido
        else:
            data = response.json()
            return data  # Resposta com status de erro

    except requests.exceptions.RequestException as e:
        # Lidar com erros de requisição, como timeout ou falha de conexão
        print(f"Request error: {e}")
        return None

#============FORMULÁRIO DE NOTIFICAÇÕES=========================#
def form_1(request):
    return render (request, 'form_notificar/form_pt_1.html')

def form_2(request): 
    data_setor = apiResponseV2(request,urlSetores, 'GET' )
    print(data_setor)
    dataIncidente = apiResponseV2(request,urltpIncidente, 'GET' )

    if request.method == "POST":

        dataEvento = request.POST.get('dataEvento')
        setorNotificador = request.POST.get('setorNotificador') 
        setorNotificado = request.POST.get('sefotNotificado')
        nomePaciente = request.POST.get('nomePaciente')
        idadePaciente = request.POST.get('idadePaciente')
        tpIncidente = request.POST.get('tpIncidente')
        eventoDescricao = request.POST.get('eventoDescricao')
        evidencia = request.FILES.get('evidencia')
        
        body_notif = {
            "dt_evento": dataEvento,
            "nm_pac": nomePaciente,
            "idade_pac": idadePaciente,
            "comentario": str(f"{eventoDescricao}"),
            "setor_notificado": str(f"{setorNotificado}"), 
            "setor_notificador": str(f"{setorNotificador}"), 
            "tp_incidente": int(f"{tpIncidente}"),
            "status": False,
        }
        if evidencia is not None:
            files = {"evidencia": evidencia}
        else:
            files = None        

        dataNotificacao = apiResponse(request, urlNotificacao_V2, 'POST', data=body_notif, file=files)

        return redirect('/notificar/form_finalizado')
    context = {
        'setores': data_setor,
        'tpIncidente': dataIncidente,
    } 
    
    return render (request, 'form_notificar/formulario_notificacao.html', context)

def form_3(request):
    return render(request, 'form_notificar/form_finalizado.html')
#===============================================================#

#================ SISTEMA DE NOTIFICAÇÃO ===========================#
def relatorio_notificar(request):
    headers = request.session.get('headers')
    ano_atual = datetime.now().year
    if headers is None:
        return render_error_404(request)
    #================== ARQUIVOS JSONS ==========================#
    dataNotificacao = apiResponse(request,f'{urlNotificacao}?year={ano_atual}', 'GET' )
    data_setor = apiResponse(request,urlSetores, 'GET' )
    dataNaoConformidade = apiResponse(request,f'{urlNaoConformidade}?year={ano_atual}', 'GET' )
    dataStatus = apiResponse(request,urlStatus, 'GET' )
    dataUsuarios = apiResponse(request,urlUsuarios, 'GET' )
    dataUsuariosV2 = apiResponse(request,urlUsuariosV2, 'GET' )
    dataTpIncidente = apiResponse(request,urltpIncidente, 'GET' )
    dataTpIndicador = apiResponse(request,urlTpIndicador, 'GET' )
    dataPlanoAcao = apiResponse(request,urlPlanoAcao, 'GET' )
    #============================================================#
    
    #============ NOTIFICAÇÃO ===================#
    for notificacoes in dataNotificacao:
        # Converter a string para um objeto datetime
        data_obj = datetime.strptime(notificacoes['dt_evento'], "%Y-%m-%d")
        data_formatada = data_obj.strftime("%d/%m/%Y")
        notificacoes['dt_evento'] = data_formatada
        for setor in data_setor:
            if notificacoes['setor_notificado'] == setor['id']:
                notificacoes['setor_notificado'] = setor['name']
            if notificacoes['setor_notificador'] == setor['id']:
                notificacoes['setor_notificador'] = setor['name']
    #=================================================#         

    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'NCONF':
            notificacao_id = request.POST.get('input_notificacao_id')
            responsavel_id = request.POST.get('responsavel')
            dataNotif = apiResponse(request,f"{urlNotificacao}{notificacao_id}/", 'GET' )
            Body_True = {
                "status": True
            }

            bodyNConform = {
                "dt_evento": dataNotif['dt_evento'],
                "nm_pac": dataNotif['nm_pac'],
                "idade_pac": dataNotif['idade_pac'],
                "comentario": dataNotif['comentario'],
                "setor_notificado":  dataNotif['setor_notificado'],
                "setor_notificador":  dataNotif['setor_notificador'],
                "responsavel": responsavel_id,
                "tp_incidente": dataNotif['tp_incidente'],
                "status": 1,
                "created_at":obter_data_hora_formatada(),
            }
            #=====================TRATATIVA DA IMAGEM===============================#
            imagem_url = dataNotif['evidencia']
            if dataNotif['evidencia'] == None:
                files = None
                dataNotif2 = apiResponse(request,f"{urlNotificacao}{notificacao_id}/", 'PUT', data=Body_True)
                dataNConformidade = apiResponse(request, urlNaoConformidade, 'POST', data=bodyNConform,file=files)
                return redirect(request.path)
            else:
                    response = requests.get(imagem_url)
            if response.status_code == 200:
                imagem_bytes = response.content
                # Converter a imagem para o formato JPEG
                imagem_pil = Image.open(BytesIO(imagem_bytes))
                imagem_pil_jpeg = imagem_pil.convert("RGB")

                # Criar um arquivo temporário para a imagem em formato JPEG
                imagem_temp = BytesIO()
                imagem_pil_jpeg.save(imagem_temp, format="JPEG")
                files = {"evidencia": ("imagem.jpg", imagem_temp.getvalue(), "image/jpeg")}
                dataNotif2 = apiResponse(request,f"{urlNotificacao}{notificacao_id}/", 'PUT', data=Body_True)
                dataNConformidade = apiResponse(request, urlNaoConformidade, 'POST', data=bodyNConform,file=files)
                return redirect(request.path)   

            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'TPINC':
            id_n_conf = request.POST.get('id_n_conf')
            tp_incidente = request.POST.get('tipo_incidente')
            body_incidente = {
                "tp_incidente": tp_incidente
            }
            dataTpIncidente = apiResponse(request,f"{urlNaoConformidade}{id_n_conf}/", 'PUT', data=body_incidente)
            return redirect(request.path)

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'Notificacoes': dataNotificacao,
        'responsaveis':dataUsuariosV2,
        'tpIncidente':dataTpIncidente,
        'tpIndicador':dataTpIndicador,
    }

    return render(request, 'relatorio_notificar.html', context)

def planoAcao(request):
    headers = request.session.get('headers')
    id_usu = request.session.get('id_usuario')
    if headers is None:
        return render_error_404(request)
    #================== ARQUIVOS JSONS ==========================#
    print(f'{urlNaoConformidade}?responsavel={id_usu}')
    dataNaoConformidade = apiResponse(request,f'{urlNaoConformidade}?responsavel={id_usu}', 'GET' )
    dataStatus = apiResponse(request,urlStatus, 'GET' )
    dataUsuarios = apiResponse(request,urlUsuarios, 'GET' )
    dataPlanoAcao = apiResponse(request,urlPlanoAcao, 'GET' )
    dataUser = apiResponse(request,f'{urlUsuarios}{id_usu}/', 'GET' )
    dataTpIncidente = apiResponse(request,urltpIncidente, 'GET' )
    data_setor = apiResponse(request,urlSetores, 'GET' )
    #============================================================#

    #================= NÃO CONFORMIDADE =========================#
    for n_conform in dataNaoConformidade:
        if n_conform['status'] == 1:
            n_conform['created_at'] = calcular_diferenca_tempo(n_conform['created_at'])
        if n_conform['status'] == 4:
            n_conform['created_at'] = calcular_tempo_entre_created_updated(n_conform)       
        for status in dataStatus:
            for usuario in dataUsuarios:
                if status['id'] == n_conform['status']:
                    n_conform['status'] = status['status']
                if usuario['id'] == n_conform['responsavel']:
                    n_conform['responsavel'] = usuario['nome']
    #============================================================#  
    for n_conform in dataNaoConformidade:
        for plAcao in dataPlanoAcao:
            for setor in data_setor:
                if n_conform['plano_acao'] == plAcao['id']:
                    n_conform['planejamento'] = plAcao
                if setor['id'] == n_conform['setor_notificado']:
                    n_conform['setor_notificado'] = setor['name']
                if setor['id'] == n_conform['setor_notificador']:
                    n_conform['setor_notificador'] = setor['name']
    #=================== PLANO DE AÇÃO ==========================#
    pprint.pprint(dataNaoConformidade)
    #============================================================#  

    if request.method == "POST":
        id_plano_acao = request.POST.get('id_plano_acao')
        id_n_conform = request.POST.get('id_n_conform')


        oQue_acao = request.POST.get('oQue_acao')
        porQue_acao = request.POST.get('porQue_acao')
        ondeAcao = request.POST.get('ondeAcao')
        quandoAcao = request.POST.get('quandoAcao')
        porQuem_acao = request.POST.get('porQuem_acao')
        comoAcao = request.POST.get('comoAcao')
        quantoAcao = request.POST.get('quantoAcao')

        if id_plano_acao:
            data_NaoConformidade = {
                "o_que": oQue_acao,
                "por_que": porQue_acao,
                "quando": quandoAcao,
                "onde": ondeAcao,
                "por_quem": porQuem_acao, 
                "quanto": quantoAcao, 
                "como": comoAcao,
                "n_conform": id_n_conform
            }
            data_plano_acao = apiResponse(request,f"{urlPlanoAcao}", 'POST', data=data_NaoConformidade)

            bod_n_conform = {
                "plano_acao": data_plano_acao['id'],
                "status": 4,
            }
            data_n_conform = apiResponse(request,f"{urlNaoConformidade}{id_n_conform}/", 'PUT', data=bod_n_conform)

            print(data_plano_acao)
            print(data_n_conform)
            return redirect(request.path)

        #Body_status={
        #    "status": 4,
        #}
        #print(id_plano_acao)
        #dataNotif2 = apiResponse(request,f"{urlNaoConformidade}{id_nconform}/", 'PUT', data=Body_status)
        #respNaoConformidade = requests.post(url=urlNaoConformidade, data=data_NaoConformidade)
        #dataRespNaoConformidade  = respNaoConformidade.json()
        return redirect(request.path)
    
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'NaoConformidade': dataNaoConformidade,
        'id_user':dataUser['nome'],
        'tpIncidente':dataTpIncidente,

    }   
    return render(request, 'planoAcao.html', context)

def cadastro_Pt1(request):
    headers = request.session.get('headers')
    if headers is None:
        return render_error_404(request)
    
    if request.method == "POST":
        tp_cad = request.POST.get('item')
        return redirect(f'/notificar/cadastro/{tp_cad}')

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    }
    return render(request, 'cadastro_pt1.html', context)

def cadastro(request, tp_cad):
    headers = request.session.get('headers')
    if headers is None:
        return render_error_404(request)
    dataTpIncidente = apiResponse(request,urltpIncidente, 'GET' )
    if request.method == "POST":
        nm_item = request.POST.get('n_item')
        id_item = request.POST.get('id_item')
        esc_cor = request.POST.get('cor_item')
        body_item = {}
        if '_method' in request.POST and request.POST['_method'] == 'ADD':
            if nm_item is not None and nm_item.strip() != '':
                body_item['tp_Incidente'] = nm_item
            if esc_cor is not None:
                body_item["tp_cor"] = esc_cor
            dataItem = apiResponse(request,f"{urltpIncidente}", 'POST', data=body_item)      
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'ALT':
            if nm_item is not None and nm_item.strip() != '':
                body_item['tp_Incidente'] = nm_item
            if esc_cor is not None:
                body_item["tp_cor"] = esc_cor
            dataItem = apiResponse(request,f"{urltpIncidente}{id_item}/", 'PUT', data=body_item)
            return redirect(request.path)
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'tpIncidente':dataTpIncidente,
    }
    return render(request, 'cadastro_pt2.html', context)

#=====================================================================#
def relatorio_notificar22(request):
    headers = request.session.get('headers')
    ano_atual = datetime.now().year
    if headers is None:
        return render_error_404(request)
    #================== ARQUIVOS JSONS ==========================#
    dataNotificacao = apiResponse(request,f'{urlNotificacao}?year={ano_atual}', 'GET' )
    data_setor = apiResponse(request,urlSetores, 'GET' )
    dataNaoConformidade = apiResponse(request,f'{urlNaoConformidade}?year={ano_atual}', 'GET' )
    dataStatus = apiResponse(request,urlStatus, 'GET' )
    dataUsuarios = apiResponse(request,urlUsuarios, 'GET' )
    dataUsuariosV2 = apiResponse(request,urlUsuariosV2, 'GET' )
    dataTpIncidente = apiResponse(request,urltpIncidente, 'GET' )
    dataTpIndicador = apiResponse(request,urlTpIndicador, 'GET' )
    dataPlanoAcao = apiResponse(request,urlPlanoAcao, 'GET' )
    #============================================================#

    
    #============ NOTIFICAÇÃO ===================#
    print(f'{urlNotificacao}?year={ano_atual}')
    print('Antes do dataNotificacao')
    for notificacoes in dataNotificacao:
        
        for setor in data_setor:
            if notificacoes['setor_notificado'] == setor['id']:
                notificacoes['setor_notificado'] = setor['name']
            if notificacoes['setor_notificador'] == setor['id']:
                notificacoes['setor_notificador'] = setor['name']
    #=================================================#        
   
    #============ NÃO CONFORMIDADE ===================#
    for n_conform in dataNaoConformidade:
        for status in dataStatus:
            for usuario in dataUsuarios:
                if status['id'] == n_conform['status']:
                    n_conform['status'] = status['status']
                if usuario['id'] == n_conform['responsavel']:
                    n_conform['responsavel'] = usuario['nome']

    for n_conform in dataNaoConformidade:
        n_conform['created_at'] = calcular_diferenca_tempo(n_conform['created_at'])
        for status in dataStatus:
            for usuario in dataUsuarios:
                for setor in data_setor:
                    if status['id'] == n_conform['status']:
                        n_conform['status'] = status['status']
                    if usuario['id'] == n_conform['responsavel']:
                        n_conform['responsavel'] = usuario['nome']
                    if setor['id'] == n_conform['setor_notificado']:
                        n_conform['setor_notificado'] = setor['name']
                    if setor['id'] == n_conform['setor_notificador']:
                        n_conform['setor_notificador'] = setor['name']
    
    #=================================================#   
         
    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'NCONF':
            notificacao_id = request.POST.get('input_notificacao_id')
            responsavel_id = request.POST.get('responsavel')
            dataNotif = apiResponse(request,f"{urlNotificacao}{notificacao_id}/", 'GET' )
            Body_True = {
                "status": True
            }

            bodyNConform = {
                "dt_evento": dataNotif['dt_evento'],
                "nm_pac": dataNotif['nm_pac'],
                "idade_pac": dataNotif['idade_pac'],
                "comentario": dataNotif['comentario'],
                "setor_notificado":  dataNotif['setor_notificado'],
                "setor_notificador":  dataNotif['setor_notificador'],
                "responsavel": responsavel_id,
                "tp_incidente": dataNotif['tp_incidente'],
                "status": 1,
                "created_at":obter_data_hora_formatada(),
            }
            #=====================TRATATIVA DA IMAGEM===============================#
            imagem_url = dataNotif['evidencia']
            if dataNotif['evidencia'] == None:
                files = None
                dataNotif2 = apiResponse(request,f"{urlNotificacao}{notificacao_id}/", 'PUT', data=Body_True)
                dataNConformidade = apiResponse(request, urlNaoConformidade, 'POST', data=bodyNConform,file=files)
                return redirect(request.path)
            else:
                    response = requests.get(imagem_url)
            if response.status_code == 200:
                imagem_bytes = response.content
                # Converter a imagem para o formato JPEG
                imagem_pil = Image.open(BytesIO(imagem_bytes))
                imagem_pil_jpeg = imagem_pil.convert("RGB")

                # Criar um arquivo temporário para a imagem em formato JPEG
                imagem_temp = BytesIO()
                imagem_pil_jpeg.save(imagem_temp, format="JPEG")
                files = {"evidencia": ("imagem.jpg", imagem_temp.getvalue(), "image/jpeg")}
                dataNotif2 = apiResponse(request,f"{urlNotificacao}{notificacao_id}/", 'PUT', data=Body_True)
                dataNConformidade = apiResponse(request, urlNaoConformidade, 'POST', data=bodyNConform,file=files)
                return redirect(request.path)   

            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'TPINC':
            id_n_conf = request.POST.get('id_n_conf')
            tp_incidente = request.POST.get('tipo_incidente')
            body_incidente = {
                "tp_incidente": tp_incidente
            }
            dataTpIncidente = apiResponse(request,f"{urlNaoConformidade}{id_n_conf}/", 'PUT', data=body_incidente)
            return redirect(request.path)

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'Notificacoes': dataNotificacao,
        'responsaveis':dataUsuariosV2,
        'tpIncidente':dataTpIncidente,
        'tpIndicador':dataTpIncidente,
        'NaoConformidade': dataNaoConformidade,
        'planoAcao':dataPlanoAcao
    }

    return render(request, 'relatorio_notificar.html', context)
