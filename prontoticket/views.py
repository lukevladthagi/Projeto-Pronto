from asyncio import DatagramTransport
from importlib.metadata import files
from re import sub
from administrativo.views import *
from django.shortcuts import render
from django.shortcuts import render, redirect
import requests, json, pprint, pytz
from datetime import datetime, timedelta, date
from django.views.decorators.cache import cache_page
from prontocheck.views import escolheSetor
from collections import defaultdict
from .utils import *
import time
from itertools import count

#====================== URLS CHECKLIST ===========================#
url_setores = f"http://{host}/setores/"
url_item_checklist = f"http://{host}/prontoticket/chkItem/"
url_Subitem_checklist = f"http://{host}/prontoticket/chkSubIt/"
url_checklist = f"http://{host}/prontoticket/checklist/"
#====================== URLS PRONTOTICKET ===========================#
url_problemas = f"http://{host}/prontoticket/problema"
url_tp_problemas = f"http://{host}/prontoticket/tpProb"
#=======================PRONTOTICKET==============================#

def chamado(request):

    """Abrir chamados entre os setores do hospital

    Parameters:
    request (request): Request recebida pelo sistema 

    Returns:
    Render: Renderização do template html
    Dict: Dicionario contendo as informações que serão visualizadas no template

    """
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    idUsuario = request.session.get('id_usuario')
    
    result = verifica_headers(request, headers)
    
    if result:
        return result
    
    dataset = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')
    dataprob = apiResponse(request ,f'http://{host}/prontoticket/problema/', 'GET')
    datalocal = apiResponse(request, f'http://{host}/prontoticket/local/', 'GET')
    dataTipoProb = apiResponse(request, f'http://{host}/prontoticket/tpProb/', 'GET')

    context = {
        'setores':dataset,
        'problemas':dataprob,
        'local':datalocal,
        'tipoProb': dataTipoProb,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }
    
    if request.method == 'POST':
        setorId = int(request.POST.get('setor'))
        setorLocal = int(request.POST.get('setorLocalSelect'))
        problemaId = request.POST.get('problema')
        tpProblema = request.POST.get('tipoProblema')
        comentario = request.POST.get('comentario')
        local = request.POST.get('localChamadoSelect')
        unidade = request.POST.get('unidade')
        paciente = request.POST.get('paciente')
        telefone = request.POST.get('contato')
        email = request.POST.get('email')
        foto = request.FILES.get('foto')
       
        dataprio = apiResponse(request, f'http://{host}/prontoticket/prioridade/?problema={problemaId}', 'GET')
        msla = ''

        if setorId == 2:
            if paciente == 'sim':
                msla = '04:00:00'
            
            elif paciente == 'nao':
                msla = '12:00:00'

        else:
            for problema in dataprob:
                if problema['id'] == int(problemaId):
                    if problema['sla'] != None: # If para evitar problema que não tem sla
                        slaId = problema['sla']
                        dataSla = apiResponse(request, f'http://192.168.4.33:8000/prontoticket/sla/{slaId}/', 'GET')
                        msla = dataSla['sla']

        prioridade = definirPrioridade(setorId, dataprio, paciente)

        chamado_data = {
            "titulo": f"{comentario}",
            "prioridade": prioridade,
            "paciente": f'{paciente}',
            "telefone": f"{telefone}",
            "email": f"{email}",
            "unidade": f"{unidade}",
            "setor_recebe": f"{setorId}",
            "setor_local": setorLocal,
            "local_setor": local,
            "problema": f"{problemaId}",
            "tp_problema": tpProblema,
            "usuario": idUsuario,
            "m_sla": msla,
            "status": 1
        }
        #print(chamado_data)
        files = {"evidencia": foto}
        print(files)
        dataresposta = apiResponse(request, f'http://{host}/prontoticket/chamado/', 'POST', data=chamado_data, file=files)
        
        context = {
            'resposta':dataresposta,
            'bloq_tela': bloq_tela,
            'nm_colaborador':request.session.get('nm_colaborador'),
        }
        idChamado = context['resposta']['id']
        return redirect(f'/prontocardio/prontoticket/confirma_chamado/{idChamado}')
    return render(request, 'abertura-chamado.html', context)

def agendarChamado(request):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    idUsuario = request.session.get('id_usuario')

    result = verifica_headers(request, headers)
    if result:
        return result

    dataset = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET') 
    dataprob = apiResponse(request, f'http://{host}/prontoticket/problema/', 'GET')
    datalocal = apiResponse(request, f'http://{host}/prontoticket/local/', 'GET')
    dataTipoProb = apiResponse(request, f'http://{host}/prontoticket/tpProb/', 'GET')
    
    context = {
        'setores':dataset,
        'problemas':dataprob,
        'local':datalocal,
        'tipoProb': dataTipoProb,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }
    
    if request.method == 'POST':
        setorId = int(request.POST.get('setor'))
        setorLocal = int(request.POST.get('setorLocalSelect'))
        problemaId = request.POST.get('problema')
        tpProblema = request.POST.get('tipoProblema')
        comentario = request.POST.get('comentario')
        local = request.POST.get('localChamadoSelect')
        unidade = request.POST.get('unidade')
        paciente = request.POST.get('paciente')
        dataAgendado = request.POST.get('dataSelecionada')
        telefone = request.POST.get('contato')
        email = request.POST.get('email')
        foto = request.FILES.get('foto')
        print(problemaId, paciente)
        
        dataprio = apiResponse(request, f'http://{host}/prontoticket/prioridade/?problema={problemaId}', 'GET')
        msla = ''

        if setorId == 2:
            if paciente == 'sim':
                msla = '04:00:00'
            
            else:
                msla = '12:00:00'
        
        else:

            for problema in dataprob:
                if problema['id'] == int(problemaId):
                    if problema['sla'] != None: # If para evitar problema que não tem sla
                        slaId = problema['sla']
                        dataSla = apiResponse(request, f'http://192.168.4.33:8000/prontoticket/sla/{slaId}/', 'GET')
                        msla = dataSla['sla']

        prioridade = definirPrioridade(setorId, dataprio, paciente)


        chamado_data = {
            "titulo": f"{comentario}",
            "email": f"{email}",
            "telefone": f"{telefone}",
            "prioridade": prioridade,
            "paciente": f'{paciente}',
            "unidade": f"{unidade}",
            "setor_recebe": setorId,
            "setor_local": setorLocal,
            "local_setor": local,
            "problema": f"{problemaId}",
            "tp_problema": tpProblema,
            "agend": f'{dataAgendado}', 
            "usuario": idUsuario,
            "m_sla": msla,
            "status": 4
        }
        files = {"evidencia": foto}
        dataresposta = apiResponse(request, f'http://{host}/prontoticket/chamado/', 'POST', data=chamado_data, file=files)
        dataAbertura = str(dataAgendado)
        dataAlteracao = str(dataAgendado)
        dataFormatada = formataData(dataAbertura, dataAlteracao, "%Y-%m-%dT%H:%M")
        dataAbertura = dataFormatada[0]
        dataresposta['agend'] = dataAbertura

        context = {
            'resposta':dataresposta,
            'bloq_tela': bloq_tela,
            'nm_colaborador':request.session.get('nm_colaborador'),
        }
        return render(request, 'chamado-realizado.html', context)
    return render(request, 'abertura-agendado.html', context)

def pesquisarChamado(request):

    #Método vai ser removido, não esta sendo utilizado, aguardando confirmação
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    if not headers:
        return render(request, 'pages-error-404.html')
    
    if request.method == 'POST':
        nchamado = request.POST.get('chamadoId')

        if nchamado != "":
            chamadoId = int(nchamado) 
            chamadoUrl = f'http://{host}/prontoticket/chamado/{chamadoId}/'
            chamadoResponse = requests.get(url=chamadoUrl, headers=headers)

            if chamadoResponse.status_code > 201:
                return render(request, "chamado-nao-encontrado.html")

            return redirect(f'/prontocardio/prontoticket/editar_chamado/{chamadoId}')
            
        else:
            return render(request, "chamado-nao-encontrado.html")
    
    context = {'bloq_tela':bloq_tela}

    return render(request, 'pesquisar-chamado.html', context)

def confirmaChamado(request, idchamado):

    """Conclusão da abertura do chamado e renderiza algumas informações do mesmo

    Parameters:
    request (request): Request recebida pelo sistema
    idchamado (int): Id do chamado que foi realizado

    Returns:
    Render: Renderização do template html
    Dict: Dicionario contendo as informações que serão visualizadas no template

    """

    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    
    result = verifica_headers(request, headers)
    if result:
        return result

    chamadoAberto = apiResponse(request, f'http://{host}/prontoticket/chamado/{idchamado}/', 'GET')

    context = {
        'resposta':chamadoAberto,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    return render(request, 'chamado-realizado.html', context)

def editarChamado(request,idchamado):

    """Modificações gerais do estado atual do chamado

    Parameters:
    request (request): Request recebida pelo sistema
    idchamado (int): Id do chamado que vai ser editado

    Returns:
    Render: Renderização do template html
    Dict: Dicionario contendo as informações que serão poderão ser modificadas

    """

    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    idUsuarioLogado = request.session.get('id_usuario')

    result = verifica_headers(request, headers)
    if result:
        return result

    datachamado = apiResponse(request, f'http://{host}/prontoticket/chamado/{idchamado}/', 'GET')
    datausuario = apiResponse(request, f'http://{host}/prontocheck/usuarios/', 'GET')
    datasetor = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')
    datalocal = apiResponse(request, f'http://{host}/prontoticket/local/', 'GET')
    dataproblema = apiResponse(request, f'http://{host}/prontoticket/problema/', 'GET')
    dataNota = apiResponse(request, f'http://{host}/prontoticket/notas/?chamado={idchamado}', 'GET')

    # Troca o id do usuario pelo nome
    idUserCham = datachamado['usuario']
    dataLogin = apiResponse(request, f'http://{host}/usuarios/{idUserCham}/', 'GET')
    datachamado['usuario'] = dataLogin['nome']
    userAtend = None

    #Condição para não extraprolar a lista de notas
    if dataNota != []:
        dataNota = dataNota[-1]
    
    # Manda o nome do responsável caso teja um
    if datachamado['usuario_atendime'] != None:
        idUserAtend = datachamado['usuario_atendime']
        dataLogin = apiResponse(request, f'http://{host}/usuarios/{idUserAtend}/', 'GET')
        userAtend = dataLogin['nome']

    # Tratativa das notas do chamado / Formatação de data
    notas = chat_chamado(request, idchamado)
    dataFormatada = formataData(datachamado['created_at'], datachamado['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
    datachamado['created_at'] = dataFormatada[0]
    datachamado['updated_at'] = dataFormatada[1]

    context = {
        key: value for key, value in {
            'chamado':datachamado,
            'notas': notas,
            'idchamado':idchamado,
            'usuarios': datausuario,
            'setores': datasetor,
            'local':datalocal,
            'problema':dataproblema,
            'userAtend': userAtend,
            'bloq_tela': bloq_tela,
            'nm_colaborador':request.session.get('nm_colaborador'),
        }.items() if value != ''
    }
    
    if request.method == 'POST':
        notaEsc = request.POST.get('notaEsc')
        nota_chamado = request.POST.get('nota_chamado')
        idChamado = datachamado['id']

        # Pedido de esclarecimento atendido
        if notaEsc is not None:
            nota_data = {
                "nota": f"{notaEsc}",
                "chamado": f"{idchamado}",
                "usuario":f"{idUsuarioLogado}"
            }
            chamadoBody = {'status': 5}

            responseEditar = apiResponse(request, f'http://{host}/prontoticket/chamado/{idchamado}/', 'PUT', data=chamadoBody)
            notaResponse = apiResponse(request, f'http://{host}/prontoticket/notas/', 'POST', data=nota_data)

        if nota_chamado is not None:
            chat_chamado(request, idChamado, nota_chamado)
    
        return redirect(request.path)
        
    return render(request, 'editar-chamado.html', context)

def editarInfo(request, idchamado):

    """Modificar informações mais especificas do chamado. Contem restrição de usuario

    Parameters:
    request (request): Request recebida pelo sistema
    idchamado (int): Id do chamado que vai ser editado

    Returns:
    Render: Renderização do template html
    Dict: Dicionario contendo as informações que serão poderão ser modificadas

    """

    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    idUsuarioLogado = request.session.get('id_usuario')

    result = verifica_headers(request, headers)
    if result:
        return result
    
    datachamado = apiResponse(request, f'http://{host}/prontoticket/chamado/{idchamado}/', 'GET')
    datausuario = apiResponse(request, f'http://{host}/usuarios/', 'GET')
    datasetor = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')
    datalocal = apiResponse(request, f'http://{host}/prontoticket/local/', 'GET')
    dataproblema = apiResponse(request, f'http://{host}/prontoticket/problema/', 'GET')
    tipoProbGeral = apiResponse(request, f'http://{host}/prontoticket/tpProb/', 'GET')
    idSetor = datachamado['setor_recebe'] 
    idProblema = datachamado['problema']
    dataTipoProb = apiResponse(request, f'http://{host}/prontoticket/tpProb/?setorId={idSetor}', 'GET')
    empresasTerc = apiResponse(request, f'http://{host}/prontoticket/empresaTerceirizada/', 'GET')

    dataAbertura = datachamado['created_at']
    dataAlteracao = datachamado['created_at']
    dataFormatada = formataData(dataAbertura, dataAlteracao, "%Y-%m-%dT%H:%M:%S.%fZ")
    dataAbertura = dataFormatada[0]
    dataAlteracao = dataFormatada[1]
    datachamado['created_at'] = dataAbertura
    datachamado['updated_at'] = dataAlteracao

    dataSetorNome = apiResponse(request, f'http://{host}/prontocheck/setor/?id={idSetor}', 'GET')
    dataTecnico = apiResponse(request, f'http://{host}/prontoticket/tecnicos/', 'GET')

    # For para adicionar o nome dos técnicos aos dados do chamado
    for item in dataTecnico:
        for usuario in datausuario:
            #Pega o nome de todos os ténicos da lista
            if item['usuario'] == usuario['id']:
                item['usuarioNome'] = usuario['nome']
            
                #Pega o nome do Ténico atual
                if datachamado['tec_responsavel'] == item['id']:
                    datachamado['tecNome'] = usuario['nome']
    
    for item in dataSetorNome:
        datachamado['setor_recebe'] = item['name']
    
    for item in dataproblema:
        if item['id'] == datachamado['problema']:
            datachamado['problema'] = item['problema']

    for item in datalocal:
        if item['id'] == datachamado['setor_local']:
            datachamado['setor_local'] = item['local']

    if datachamado['usuario_atendime'] != None:
        idUserAtend = datachamado['usuario_atendime']
        dataLogin = apiResponse(request, f'http://{host}/usuarios/{idUserAtend}/', 'GET')
        userAtend = dataLogin['nome']

        context = {
            'chamado':datachamado,
            'idchamado':idchamado,
            'usuarios': datausuario,
            'usuarioLogado': idUsuarioLogado,
            'setores': datasetor,
            'local':datalocal,
            'problema':dataproblema,
            'userAtend': userAtend,
            'tipoProb': dataTipoProb,
            'tipoProbGeral': tipoProbGeral,
            'setorId': idSetor,
            'problemaId': idProblema,
            'tecnicos': dataTecnico,
            'empresas': empresasTerc,
            'bloq_tela': bloq_tela,
            'nm_colaborador':request.session.get('nm_colaborador'),
        }

    else:
        
        context = {
            'chamado':datachamado,
            'idchamado':idchamado,
            'usuarioLogado': idUsuarioLogado,
            'usuarios': datausuario,
            'setores': datasetor,
            'local':datalocal,
            'problema':dataproblema,
            'tipoProb': dataTipoProb,
            'tipoProbGeral': tipoProbGeral,
            'setorId': idSetor,
            'problemaId': idProblema,
            'tecnicos': dataTecnico,
            'empresas': empresasTerc,
            'bloq_tela': bloq_tela,
            'nm_colaborador':request.session.get('nm_colaborador'),
        }

    if request.method == 'POST':
        unidade = request.POST.get('unidade')
        setorResponsavel = request.POST.get('setor')
        setorLocal = request.POST.get('setorLocalSelect')
        problema = request.POST.get('problema')
        tpProblema = request.POST.get('tpProb')
        if type(problema) == int:
            problema = int(problema)
        
        local = request.POST.get('localChamadoSelect')
        if type(local) == str:
            local = int(local)
        possuiPaciente = request.POST.get('paciente')
        dataAgendado = request.POST.get('dataAgend')
        print(dataAgendado, type(dataAgendado))
        if dataAgendado == "":
            print("PASSOu")

        tipoCompra = request.POST.get('tipoCompra')
        dataCompra = request.POST.get('compraAgend')
        motivoCompra = request.POST.get('compraTexto')

        realiza = request.POST.get('realizarSelect')
        if realiza != None:
            realiza = int(realiza)

        escalaEquipe = request.POST.get('escalaEquipe')
        equipeObs = request.POST.get('equipeObs')

        terceAgend = request.POST.get('terceAgend')
        terceObs = request.POST.get('terceObs')
        tecResponsavel = request.POST.get('tecnicoSelect')
        tecEquipe = request.POST.get('tecResponsavel')
        empresaTerc = request.POST.get('empresaTerc')
        solicitante = request.POST.get('solicitanteSelect')
        responsavel = request.POST.get('responsavelSelect')
        print(responsavel, type(responsavel), "RESPONSAVEL")

        idChamado = datachamado['id']
        data = apiResponse(request, f'http://{host}/prontoticket/prioridade/', 'GET')
        prioridade = ''


        #Tratativa das horas da manutenção com compras
        if tipoCompra == str(1):
            sla = '360:00:00'

        elif tipoCompra == str(2):
            sla = '48:00:00'
        
        else:
            sla = datachamado['m_sla']

        # Caso de conter compra
        if dataCompra != '':
            nota_data = {
                "nota": f"{motivoCompra}",
                "chamado": f"{idchamado}",
                "usuario":f"{idUsuarioLogado}"
            }
            compraBody = {'agend': dataCompra, 'status': 4, 'usuario_atendime': idUsuarioLogado}
            notaResponse = apiResponse(request, f'http://{host}/prontoticket/notas/', 'POST', data=nota_data)
            responseEditar = apiResponse(request, f'http://{host}/prontoticket/chamado/{idChamado}/', 'PUT', data=compraBody)

        # Caso de Equipe
        elif equipeObs != '':
            nota_data = {
                "nota": f"{equipeObs}",
                "chamado": f"{idchamado}",
                "usuario":f"{idUsuarioLogado}"
            }
            equipeBody = {'agend': escalaEquipe, 'status': 4, 'tec_responsavel': tecEquipe}

            responseEditar = apiResponse(request, f'http://{host}/prontoticket/chamado/{idChamado}/', 'PUT', data=equipeBody)
            notaResponse = apiResponse(request, f'http://{host}/prontoticket/notas/', 'POST', data=nota_data)

        # Caso de terceirizado
        elif terceAgend != '':
            print("ENTROU AQUI")
            nota_data = {
                "nota": f"{terceObs}",
                "chamado": f"{idchamado}",
                "usuario":f"{idUsuarioLogado}"
            }
            equipeBody = {'agend': terceAgend, 'status': 4, 'empresa_ter': empresaTerc}

            responseEditar = apiResponse(request, f'http://{host}/prontoticket/chamado/{idChamado}/', 'PUT', data=equipeBody)
            notaResponse = apiResponse(request, f'http://{host}/prontoticket/notas/', 'POST', data=nota_data)

        if possuiPaciente != '':
            if possuiPaciente == 'sim':
                prioridade = 'alta'
            else:
                prioridade = 'baixa'

        chamadoBody = {
            key: value for key, value in {
                'prioridade': f'{prioridade}',
                'unidade': unidade,
                'setor_recebe': setorResponsavel,
                'agend': dataAgendado,
                'setor_local': setorLocal,
                'local_setor': local,
                'problema': problema,
                'tp_problema': tpProblema,
                'paciente': f'{possuiPaciente}',
                'tec_responsavel': tecResponsavel,
                'm_sla': sla,
                'usuario': solicitante,
                'usuario_atendime': responsavel
            }.items() if value != ''
        }

        if dataAgendado != "": 
            chamadoBody['status'] = 4

        responseEditar = apiResponse(request, f'http://{host}/prontoticket/chamado/{idChamado}/', 'PUT', data=chamadoBody)
        return redirect(f'/prontocardio/prontoticket/editar_chamado/{idchamado}')
    return render(request, 'editar-info.html', context)

def listarChamado(request, chamado= None):

    """Lista os chamados ainda não finalizados
    
    Parameters:
    request (request): Request recebida pelo sistema

    Returns:
    Render: Renderização do template html
    Dict: Dicionario contendo os chamados ainda não finalizados

    """
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    dataSetor = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')
    dataProblemas = apiResponse(request, f'http://{host}/prontoticket/problema/', 'GET')
    dataUsuario = apiResponse(request, f'http://{host}/usuarios/', 'GET')
    groups = ', '.join(map(str, bloq_tela))

    #Tratativa do filtro de status
    if chamado != None:
        dataChamado = chamado
    else:
        dataChamado = apiResponse(request, f'http://{host}/prontoticket/chamados_pendentes/?setor_recebe={groups}', 'GET')

    resultados = contar_chamados(request)
    dataChamadoProcessado = processar_chamados(request, dataChamado, dataSetor, dataProblemas, host)
    context = {
        'setores':dataSetor,
        'usuarios': dataUsuario,
        'dados': dataChamadoProcessado,
        'contagem': resultados,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }
    return render(request, 'listar-chamado.html', context)

def atenderFinalizar(request, idchamado):
    headers = request.session.get('headers')
    idUsuario = request.session.get('id_usuario')

    result = verifica_headers(request, headers)
    if result:
        return result
    
    username = request.session.get('nm_colaborador')
    datachamado = apiResponse(request, f'http://{host}/prontoticket/chamado/{idchamado}/', 'GET')
    dataIdUsuario = apiResponse(request, f'http://{host}/prontocheck/usuarios/?username={username}', 'GET')

    if datachamado['status'] == 1:

        chamadoBody = {
            'usuario_atendime': idUsuario,
            'status': 3,
        }
        responseEditar = apiResponse(request, f'http://{host}/prontoticket/chamado/{idchamado}/', 'PUT', data=chamadoBody)
        return redirect(f'/prontocardio/prontoticket/editar_chamado/{idchamado}')
    
    elif datachamado['status'] == 3:
        tempo = tempo_ocorrido(datachamado)
        
        chamadoBody = {
            'usuario_atendime': idUsuario,
            'status': 2,
            't_co': tempo,
        }

        responseEditar = apiResponse(request, f'http://{host}/prontoticket/chamado/{idchamado}/', 'PUT', data=chamadoBody)
        return redirect(f'/prontocardio/prontoticket/editar_chamado/{idchamado}')
        
    elif datachamado['status'] == 4:
        
        chamadoBody = {
            'usuario_atendime': idUsuario,
            'status': 3,
            'agend': '',
        }

        responseEditar = apiResponse(request, f'http://{host}/prontoticket/chamado/{idchamado}/', 'PUT', data=chamadoBody)
        return redirect(f'/prontocardio/prontoticket/editar_chamado/{idchamado}')

def notaInformativa(request,idchamado):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    idUsuario = request.session.get('id_usuario')

    result = verifica_headers(request, headers)
    if result:
        return result
    
    chamadoId = int(idchamado)
    datachamado = apiResponse(request, f'http://{host}/prontoticket/chamado/{chamadoId}/', 'GET')

    if len(datachamado) <= 0:
        return render(request, "chamado-nao-encontrado.html")
    else:
        if request.method == 'POST':
            nota = request.POST.get('nota')
            nota_data = {
                "nota": f"{nota}",
                "chamado": f"{idchamado}",
                "usuario":f"{idUsuario}"
            }

            responseEditar = apiResponse(request, f'http://{host}/prontoticket/chamado/{chamadoId}/', 'PUT')
            dataNota = apiResponse(request, f'http://{host}/prontoticket/notas/', 'POST', data=nota_data)
            
            context = {
                'chamado':datachamado,
                'bloq_tela': bloq_tela,
                'nm_colaborador':request.session.get('nm_colaborador'),
            }

            return redirect(f'/prontocardio/prontoticket/nota_realizada/{idchamado}')

        context = {
            'chamado':datachamado,
            'bloq_tela': bloq_tela,
            'nm_colaborador':request.session.get('nm_colaborador'),
        }
    
        return render(request, 'nota-informativa.html', context)

def notaRealizada(request, idchamado):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')

    result = verifica_headers(request, headers)
    if result:
        return result
    
    chamadoNota = apiResponse(request, f'http://{host}/prontoticket/chamado/{idchamado}/', 'GET')

    context = {
        'chamado':chamadoNota,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }
    return render(request, 'nota-realizada.html', context)

def chat_chamado(request, idchamado, nota= None):

    if nota == None:

        notaChamado = apiResponse(request, f'http://{host}/prontoticket/notas/?chamado={idchamado}', 'GET')
        
        for item in notaChamado:
            dataNotaFormatada = formataData(item['created_at'], item['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
            item['created_at'] = dataNotaFormatada[0]
            item['updated_at'] = dataNotaFormatada[1]
            idUserCham = item['usuario']
            dataLogin = apiResponse(request, f'http://{host}/usuarios/{idUserCham}/', 'GET')
            item['updated_at'] = dataLogin['nome']
            

        return notaChamado

    else:
        print('2')
        idUsuarioLogado = request.session.get('id_usuario')

        nota_data = {
            "nota": f"{nota}",
            "chamado": f"{idchamado}",
            "usuario":f"{idUsuarioLogado}"
        }
        notaResponse = apiResponse(request, f'http://{host}/prontoticket/notas/', 'POST', data=nota_data)
        
def tempoSla(slaTime, created_at, typeAg):

    now = datetime.now()

    #Formata  string de abertura para o formato de tempo do brasil
    if typeAg == 'abertura':

        date_string = created_at
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        created_at_formated = datetime.strptime(date_string, date_format)
        br_tz = pytz.timezone('America/Sao_Paulo')
        utc_abertura = pytz.utc.localize(created_at_formated)
        br_abertura = utc_abertura.astimezone(br_tz)
        br_abertura = br_abertura.astimezone().replace(tzinfo=None)
    
    else:
        date_string = created_at
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        created_at_formated = datetime.strptime(date_string, date_format)
        br_abertura = created_at_formated

    #Faz o calculo do tempo que ja passou da abertura do chamado ate o tempo atual
    time_difference = now - br_abertura
    return time_difference

def dash(request):
    
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    if not headers:
        return render(request, 'pages-error-404.html')
    
    dataChamado = apiResponse(request, f'http://{host}/prontoticket/chamado/', 'GET')
    dataSetor = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')
    dataProblemas = apiResponse(request, f'http://{host}/prontoticket/problema/', 'GET')

    """ chamadoStatus = filtro(request)
    abertoCnt = chamadoStatus[0]
    andamentoCnt = chamadoStatus[1]
    agendadoCnt = chamadoStatus[3]
    finalizadoCnt = chamadoStatus[2]
    agEscCnt = chamadoStatus[4]
    agValCnt = chamadoStatus[5]
    geralCnt = sum([abertoCnt, andamentoCnt, agendadoCnt, agEscCnt, agValCnt])
    #chamadoSetorDict = chamadoPorSetor(request)
    chamadoPmes = statusPorMes(request, dataChamado)
    print(chamadoPmes) """

    #TODO: Passar chamadoPmes pro template e tratar o resto por la

    context = {
        """ 'aber': abertoCnt,
        'prog': andamentoCnt,
        'agen': agendadoCnt,
        'escl': agEscCnt,
        'finl': finalizadoCnt,
        'vali': agValCnt,
        'dados': dataChamado,
        'geralCnt': geralCnt,
        #'chamadoSetor': chamadoSetorDict,
        'chamadoPmes': chamadoPmes, """
        'setores': dataSetor,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    return render (request, 'dash.html', context)

def redirecionaCadTec(request):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')

    result = verifica_headers(request, headers)
    if result:
        return result

    dataSetor = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')

    if request.method == 'POST':
        setorId = request.POST.get('setor')
        return redirect(f'/prontocardio/prontoticket/cadastro_tec/{setorId}')

    context = {
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
        'setores': dataSetor,
    }
    return render(request, 'redirec-cad-tec.html', context)

def cadastroTec(request, idSetor):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')

    result = verifica_headers(request, headers)
    if result:
        return result
    
    dataSetor = apiResponse(request, f'http://{host}/setores/', 'GET')
    dataTec = apiResponse(request, f'http://{host}/prontoticket/tecnicos/?setor={idSetor}', 'GET')
    dataUser = apiResponse(request, f'http://{host}/usuarios/', 'GET')

    #Novo modo de tratar os nomes, futuramente transformar em um função para reduzir as iterações redundantes
    dictSetor = {itemSet['id']: itemSet['name'] for itemSet in dataSetor}
    print(dictSetor)

    for itemTec in dataTec:
        itemTec['nomeSetor'] = dictSetor.get(itemTec['setor'], None)


    for itemTec in dataTec:
        for itemUser in dataUser:
            if itemTec['usuario'] == itemUser['id']:
                itemTec['nome'] = itemUser['nome']
    
    if request.method == 'POST':
        #Condições referentes a adição e edição de itens
        if '_method' in request.POST and request.POST['_method'] == 'D':
            tecId = request.POST.get('tecId')

            print(f'esse é o novo tecnico {tecId}')

            tec_body = {
                'usuario': tecId,
                'setor': idSetor
            }
            pprint.pprint(tec_body)

            apiResponse(request, f'http://{host}/prontoticket/tecnicos/', 'POST', data=tec_body)
            return redirect(request.path)

        elif '_method' in request.POST and request.POST['_method'] == 'D_ALT':
            tecId = request.POST.get('idTecEdit')
            print(tecId, "ID")
            setorTec = request.POST.get('setorLocalEdit')
            if setorTec != '':
                setorTec = int(setorTec)
            #print(f'novo setor {setorTec}, id {tecId}')

            tec_body = {
                key: value for key, value in {
                    "setor": setorTec,
                }.items() if value != ''
            }
            #print(tec_body)
            apiResponse(request, f'http://{host}/prontoticket/tecnicos/{tecId}/', 'PUT', data=tec_body)
            return redirect(request.path)
        
        elif '_method' in request.POST and request.POST['_method'] == 'D_DEL':
            tecId = request.POST.get('idTecDelete')
            print(tecId, "ID")
           
            apiResponse(request, f'http://{host}/prontoticket/tecnicos/{tecId}/', 'DEL')
            return redirect(request.path)


    context = {
        'setores': dataSetor,
        'setor': idSetor,
        'tecnicos': dataTec,
        'usuarios': dataUser,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }
    return render(request, 'cadastro-tecnico.html', context)

def empresaTerceirizada(request):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')

    result = verifica_headers(request, headers)
    if result:
        return result

    empresasTerc = apiResponse(request, f'http://{host}/prontoticket/empresaTerceirizada/', 'GET')
    print(empresasTerc)


    if request.method == 'POST':
        #Condições referentes a adição e edição de itens
        if '_method' in request.POST and request.POST['_method'] == 'D':
            nomeEmpresa = request.POST.get('nomeEmpresa')
            print(f'esse é o novo item{nomeEmpresa}')

            empresaBody = {
                "nome": nomeEmpresa,
            }

            apiResponse(request, f'http://{host}/prontoticket/empresaTerceirizada/', 'POST', data=empresaBody)
            return redirect(request.path)

        elif '_method' in request.POST and request.POST['_method'] == 'D_ALT':
            itemId = request.POST.get('idEmpresaEdit')
            novoMome = request.POST.get('novoNomeEmpresa')
            print(f'esse é o novo nome do item {novoMome}, com o Id {itemId}')

            empresaBody = {
                key: value for key, value in {
                    "nome": novoMome,
                }.items() if value != ''
            }

            apiResponse(request, f'http://{host}/prontoticket/empresaTerceirizada/{itemId}/', 'PUT', data=empresaBody)

            return redirect(request.path)

        elif '_method' in request.POST and request.POST['_method'] == 'D_DEL':
            idEmpresaDelete = request.POST.get('idEmpresaDelete')

            apiResponse(request, f'http://{host}/prontoticket/empresaTerceirizada/{idEmpresaDelete}/', 'DEL')
            return redirect(request.path)


    context = {
        'empresas': empresasTerc,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    return render(request, 'cad_empresa.html', context)

def slas(request):
    headers = request.session.get('headers')

    result = verifica_headers(request, headers)
    if result:
        return result
    
    dataSetor = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')

    if request.method == 'POST':
        setorId = request.POST.get('setor')
        return redirect(f'/prontocardio/prontoticket/slas_pt2/{setorId}')

    context = {
        'bloq_tela': request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'setores': dataSetor,
    }
    return render(request,'sla.html', context)

def slas_pt2(request,idSetor):
    headers = request.session.get('headers')
    if not headers:
        return render(request, 'pages-error-404.html')
    #===============================================================================#
    dataSetor = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')
    dataProb = apiResponse(request, f'http://{host}/prontoticket/problema/?setor_id={idSetor}', 'GET')
    dataTbProb = apiResponse(request, f'http://{host}/prontoticket/tpProb/?setor_id={idSetor}', 'GET')
    dataSla = apiResponse(request, f'http://{host}/prontoticket/sla/', 'GET')
    #===============================================================================#
    
    for item in dataProb:
        for item2 in dataTbProb:
            for item3 in dataSla:
                if item['tipoProblema'] == item2['id']:
                    item['tipoProblema'] = item2['tipoProb']
                if item['sla'] == item3['id_sla']:
                    item['sla'] = item3['sla']

    for item in dataTbProb:
        for item2 in dataProb:
            if item['problema_id'] == item2['id']:
                item['problema_id'] = item2['problema']

    if request.method == 'POST':
        body_itens = {}
        id_problema = request.POST.get('id_problema')
        id_tp_problema = request.POST.get('id_tp_problema')
        if '_method' in request.POST and request.POST['_method'] == 'TP_PROB': 
            problema_id = request.POST.get('problema_id')
            tp_problema = request.POST.get('n_tp_prob')
            print(f'id do problema para alterar:{problema_id}')
            print(f'id do tipo de problema:{id_tp_problema}')

            if problema_id:
                body_itens["problema_id"] = problema_id
            if tp_problema:
                body_itens["tipoProb"] = tp_problema
            print(body_itens)
            dataTpProblema = apiResponse(request,f'http://{host}/prontoticket/tpProb/{id_tp_problema}/', 'PUT', data=body_itens)
            print(dataTpProblema)
            print(f'http://{host}/prontoticket/tpProb/{problema_id}/')
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'PROBLEMA':
            problema_id = request.POST.get('problema_id')
            problema = request.POST.get('n_prob')
            Tp_ProbId = request.POST.get('tp_prob_id')
            tempo_sla = request.POST.get('tempo_sla')
            if problema:
                body_itens["problema"] = problema
            if Tp_ProbId:
                body_itens["tipoProblema"] = Tp_ProbId
            print(problema_id)
            print(problema)
            print(Tp_ProbId)
            print(tempo_sla)
        if '_method' in request.POST and request.POST['_method'] == 'ADD_PROBLEMA':
            nome_problema = request.POST.get('n_prob')
            tipo_problema_novo = request.POST.get('tp_prob_id')
            tempo_sla_novo = request.POST.get('id_sla')
            print(tempo_sla_novo)
            if nome_problema:
                body_itens["problema"] = nome_problema
            if tipo_problema_novo:
                body_itens["tipoProblema"] = tipo_problema_novo
            if tempo_sla_novo:
                body_itens["sla"] = tempo_sla_novo
            print(body_itens)
            dataTpProblema = apiResponse(request,f'http://{host}/prontoticket/problema/', 'POST', data=body_itens)
            return redirect(request.path)


    context = {
        'bloq_tela': request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'dataProb':dataProb,
        'dataTbProb':dataTbProb,
        'dataSla':dataSla,
    }
    return render(request,'sla_pt2.html', context)

#======================= Métodos Auxiliares ==============================#
def definirPrioridade(setorId, dataprio, paciente=None):
    print(dataprio)
    
    if setorId == 2 or setorId == 3 or setorId == 23:
        if paciente == 'sim':
            prioridade = 'alta'
            return prioridade

        elif paciente == 'nao':
            prioridade = 'baixa'
            return prioridade

    else:

        if len(dataprio) > 0:
            prioridade = dataprio[0]['prioridade']    
      
        else:
            prioridade = 'baixa'
            return prioridade

def statusPorMes(request, dataChamado):
    mesesCntDict = defaultdict(int)

    for chamado in dataChamado:
        data = chamado['created_at']
        dataFormat = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%f%z")
        ano = dataFormat.year
        mes = dataFormat.month
        mesesCntDict[(ano, mes)] += 1
    

    chamadoMesesJson = []
    for (year, month), count in mesesCntDict.items():
        chamadoMesesJson.append({
            "year": year,
            "month": month,
            "count": count
        });

    
    return json.dumps(chamadoMesesJson)

#======================= Métodos dos usuários ============================#
def chamadoUsuario(request):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    idUsuario = int(request.session.get('id_usuario'))

    result = verifica_headers(request, headers)
    if result:
        return result

    dataset = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')
    dataprob = apiResponse(request, f'http://{host}/prontoticket/problema/', 'GET')
    datalocal = apiResponse(request, f'http://{host}/prontoticket/local/', 'GET')
    dataTipoProb = apiResponse(request, f'http://{host}/prontoticket/tpProb/', 'GET')

    context = {
        'setores':dataset,
        'problemas':dataprob,
        'local':datalocal,
        'tipoProb': dataTipoProb,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }
    
    if request.method == 'POST':
        setorId = int(request.POST.get('setor'))
        setorLocal = int(request.POST.get('setorLocalSelect')) 
        problemaId = request.POST.get('problema')
        tpProblema = request.POST.get('tipoProblema')
        comentario = request.POST.get('comentario')
        local = request.POST.get('localChamadoSelect')
        unidade = request.POST.get('unidade')
        paciente = request.POST.get('paciente')
        telefone = request.POST.get('contato')
        email = request.POST.get('email')
        foto = request.FILES.get('foto')

        dataprio = apiResponse(request, f'http://{host}/prontoticket/prioridade/?problema={problemaId}', 'GET')
        msla = ''

        if setorId == 2:
            if paciente == 'sim':
                msla = '04:00:00'
            
            elif paciente == 'nao':
                msla = '12:00:00'

        else:
            for problema in dataprob:
                if problema['id'] == int(problemaId):
                    if problema['sla'] != None: # If para evitar problema que não tem sla
                        slaId = problema['sla']
                        dataSla = apiResponse(request, f'http://192.168.4.33:8000/prontoticket/sla/{slaId}/', 'GET')
                        msla = dataSla['sla']

        prioridade = definirPrioridade(setorId, dataprio, paciente)

        chamado_data = {
            "titulo": f"{comentario}",
            "prioridade": prioridade,
            "paciente": f'{paciente}',
            "telefone": f"{telefone}",
            "email": f"{email}",
            "unidade": f"{unidade}",
            "setor_recebe": f"{setorId}",
            "setor_local": setorLocal,
            "local_setor": local,
            "problema": f"{problemaId}",
            "tp_problema": tpProblema,
            "usuario": idUsuario,
            "m_sla": msla,
            "status": 1
        }
        files = {"evidencia": foto}
        dataresposta = apiResponse(request, f'http://{host}/prontoticket/chamado/', 'POST', data=chamado_data, file=files)
        context = {
            'resposta':dataresposta,
            'bloq_tela': bloq_tela,
            'nm_colaborador':request.session.get('nm_colaborador'),
        }
        idChamado = context['resposta']['id']
        return redirect(f'/prontocardio/prontoticket/confirma_chamado_usuario/{idChamado}')
    return render(request, 'abertura-chamado-usuario.html', context)

def confirmaChamadoUsuario(request, idchamado):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')

    result = verifica_headers(request, headers)
    if result:
        return result

    chamadoAberto = apiResponse(request, f'http://{host}/prontoticket/chamado/{idchamado}/', 'GET')

    context = {
        'resposta':chamadoAberto,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    return render(request, 'chamado-realizado-usuario.html', context)

def listarChamadoUsuario(request, chamado= None):
    headers = request.session.get('headers')
    idUsuario = request.session.get('id_usuario')
    bloq_tela = request.session.get('id_setor')
    dataSetor = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')
    dataUsuario = apiResponse(request, f'http://{host}/usuarios/', 'GET')
    dataProblemas = apiResponse(request, f'http://{host}/prontoticket/problema/', 'GET')
    print(bloq_tela)

    """ chamadoFiltro = None

    if request.method == 'POST':
        status = request.POST.get('status')
        coluna = request.POST.get('coluna')
        itensSelect = request.POST.get('itensSelect')

        if itensSelect != None and status != '':
            pass

        elif itensSelect != None:
            #Mudar para os pendentes
            print("2---------")
            print(coluna, itensSelect)
            idUsuario = request.session.get('id_usuario')
            chamadoFiltro = apiResponse(request, f'http://{host}/prontoticket/chamado/?{coluna}={itensSelect}&usuario={idUsuario}', 'GET')
            print(f'http://{host}/prontoticket/chamado/?{coluna}={itensSelect}&usuario={idUsuario}')
            print(chamadoFiltro)

        elif status != '':
            idUsuario = request.session.get('id_usuario')
            chamadoFiltro = apiResponse(request, f'http://{host}/prontoticket/chamado/?status={status}&usuario={idUsuario}', 'GET') """

    #Tratativa do filtro de status
    if chamado != None:
        dataChamado = chamado
    else:
        dataChamado = apiResponse(request, f'http://{host}/prontoticket/chamados_pendentes/?usuario={idUsuario}', 'GET')

    resultados = contar_chamados(request,  idUsuario)
    dataChamadoProcessado = processar_chamados(request, dataChamado, dataSetor, dataProblemas, host)
    
    context = {
        'dados': dataChamadoProcessado,
        'setores':dataSetor,
        'usuarios': dataUsuario,
        'contagem': resultados,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    return render(request, 'listar-chamado-usuario.html', context)

def editarChamadoUsuario(request,idchamado):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    idUsuarioLogado = request.session.get('id_usuario')

    result = verifica_headers(request, headers)
    if result:
        return result

    datachamado = apiResponse(request, f'http://{host}/prontoticket/chamado/{idchamado}/', 'GET')
    datausuario = apiResponse(request, f'http://{host}/prontocheck/usuarios/', 'GET')
    datasetor = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')
    datalocal = apiResponse(request, f'http://{host}/prontoticket/local/', 'GET')
    dataproblema = apiResponse(request, f'http://{host}/prontoticket/problema/', 'GET')
    dataNota = apiResponse(request, f'http://{host}/prontoticket/notas/?chamado={idchamado}', 'GET')

    # Troca o id do usuario pelo nome
    idUserCham = datachamado['usuario']
    dataLogin = apiResponse(request, f'http://{host}/usuarios/{idUserCham}/', 'GET')
    datachamado['usuario'] = dataLogin['nome']
    userAtend = None

    #Condição para não extraprolar a lista de notas
    if dataNota != []:
        dataNota = dataNota[-1]

    # Manda o nome do responsável caso teja um
    if datachamado['usuario_atendime'] != None:
        idUserAtend = datachamado['usuario_atendime']
        dataLogin = apiResponse(request, f'http://{host}/usuarios/{idUserAtend}/', 'GET')
        userAtend = dataLogin['nome']

    # Tratativa das notas do chamado / Formatação de data
    notas = chat_chamado(request, idchamado)
    dataFormatada = formataData(datachamado['created_at'], datachamado['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
    datachamado['created_at'] = dataFormatada[0]
    datachamado['updated_at'] = dataFormatada[1]

    context = {
        key: value for key, value in {
            'chamado':datachamado,
            'notas': notas,
            'idchamado':idchamado,
            'usuarios': datausuario,
            'setores': datasetor,
            'local':datalocal,
            'problema':dataproblema,
            'userAtend': userAtend,
            'bloq_tela': bloq_tela,
            'nm_colaborador':request.session.get('nm_colaborador'),
        }.items() if value != ''
    }
    
    if request.method == 'POST':
        notaAvaliacao = request.POST.get('notaAvaliacao')
        textoAceita = request.POST.get('textoAceita')
        textoRejeita = request.POST.get('textoRejeita')
        notaEsc = request.POST.get('notaEsc')
        nota_chamado = request.POST.get('nota_chamado')
        idSetor = datachamado['setor_recebe']
        idChamado = datachamado['id']
        idUserChamado = datachamado['usuario']
        chamadoStatus = datachamado['status']


        if nota_chamado is not None:
            print("HA")
            chat_chamado(request, idChamado, nota_chamado)
            return redirect(request.path)

        # Pedido de esclarecimento atendido
        if notaEsc is not None:
            nota_data = {
                "nota": f"{notaEsc}",
                "chamado": f"{idchamado}",
                "usuario":f"{idUsuarioLogado}"
            }
            chamadoBody = {'status': 3}

            responseEditar = apiResponse(request, f'http://{host}/prontoticket/chamado/{idchamado}/', 'PUT', data=chamadoBody)
            notaResponse = apiResponse(request, f'http://{host}/prontoticket/notas/', 'POST', data=nota_data)
            return redirect(request.path)
        
        # Aceitou a validação
        if textoAceita is not None:
            avalBody = {
                'setor': idSetor,
                'notaSetor': notaAvaliacao,
                'comentario': textoAceita
            }
            avalResponse = apiResponse(request, f'http://{host}/nps/setores/', 'POST', data=avalBody)
            now = str(datetime.now())
            chamadoStatus = {'status': 2, 'dt_finalizado': now}
            responseEditar = apiResponse(request, f'http://{host}/prontoticket/chamado/{idChamado}/', 'PUT', data=chamadoStatus)
            return redirect(request.path)

        # Não aceitou a validação
        elif textoRejeita is not None:
            nota_body = {
                "nota": textoRejeita,
                "chamado": idChamado,
                "usuario": idUsuarioLogado
            }

            chamado_body = {
                'status': 1,
                "agend": None
            }
            responseEditar = apiResponse(request, f'http://{host}/prontoticket/chamado/{idChamado}/', 'PUT', data=chamado_body)
            notaResponse = apiResponse(request, f'http://{host}/prontoticket/notas/', 'POST', data=nota_body)
            return redirect(request.path)

    return render(request, 'editar-chamado-usuario.html', context)

def notaInformativaUsuario(request,idchamado):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    idUsuario = request.session.get('id_usuario')

    result = verifica_headers(request, headers)
    if result:
        return result
    
    chamadoId = int(idchamado)
    datachamado = apiResponse(request, f'http://{host}/prontoticket/chamado/{chamadoId}/', 'GET')

    if len(datachamado) <= 0:
        return render(request, "chamado-nao-encontrado.html")
    else:
        if request.method == 'POST':
            nota = request.POST.get('nota')
            nota_data = {
                "nota": f"{nota}",
                "chamado": f"{idchamado}",
                "usuario":f"{idUsuario}"
            }

            responseEditar = apiResponse(request, f'http://{host}/prontoticket/chamado/{chamadoId}/', 'PUT')
            dataNota = apiResponse(request, f'http://{host}/prontoticket/notas/', 'POST', data=nota_data)
            
            context = {
                'chamado':datachamado,
                'bloq_tela': bloq_tela,
                'nm_colaborador':request.session.get('nm_colaborador'),
            }

            return redirect(f'/prontocardio/prontoticket/nota_realizada_usuario/{idchamado}')

        context = {
            'chamado':datachamado,
            'bloq_tela': bloq_tela,
            'nm_colaborador':request.session.get('nm_colaborador'),
        }
        return render(request, 'nota-informativa-usuario.html', context)

def notaRealizadaUsuario(request, idchamado):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')

    result = verifica_headers(request, headers)
    if result:
        return result

    chamadoNota = apiResponse(request, f'http://{host}/prontoticket/chamado/{idchamado}/', 'GET')

    context = {
        'chamado':chamadoNota,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }
    return render(request, 'nota-realizada-usuario.html', context)

def pesquisarChamadoUsuario(request):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')

    result = verifica_headers(request, headers)
    if result:
        return result
    
    if request.method == 'POST':
        nchamado = request.POST.get('chamadoId')

        if nchamado != "":
            chamadoId = int(nchamado) 
            chamadoUrl = f'http://{host}/prontoticket/chamado/{chamadoId}/'
            chamadoResponse = requests.get(url=chamadoUrl, headers=headers)

            if chamadoResponse.status_code > 201:
                return render(request, "chamado-nao-encontrado.html")

            return redirect(f'/prontocardio/prontoticket/editar_chamado_usuario/{chamadoId}')
            
        else:
            return render(request, "chamado-nao-encontrado.html")
    
    context = {
        'bloq_tela':bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    return render(request, 'pesquisar-chamado-usuario.html', context)

#======================= Checklist prontoticket ============================#

def setorChecklist(request):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')

    result = verifica_headers(request, headers)
    if result:
        return result

    dataset = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')
    dataItem = apiResponse(request, f'http://{host}/prontoticket/chkItem/', 'GET')
  
    context = {
        'setores':dataset,
        'itens':dataItem,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    if request.method == 'POST':
        setorId = request.POST.get('setor')
        return redirect(f'/prontocardio/prontoticket/redireciona_checklist_pt2/{setorId}')

    return render(request, 'checklist/redirec_checklist.html', context) 

def setorChecklist_pt2(request, idSetor):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')

    result = verifica_headers(request, headers)
    if result:
        return result

    dataset = apiResponse(request, f'http://{host}/prontocheck/setor/{idSetor}/', 'GET')
    datalocal = apiResponse(request, f'http://{host}/prontoticket/local/?setor={idSetor}', 'GET')

    context = {
        'setor':dataset,
        'local':datalocal,
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    if request.method == 'POST':
        local = request.POST.get('local')
        print(f'O local que foi escolhido{local}')
        return redirect(f'/prontocardio/prontoticket/checklist/{idSetor}/{local}')

    return render(request, 'checklist/redirec_checklist_pt2.html', context)        

def checklist(request, local_id ,idSetor):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    
    result = verifica_headers(request, headers)
    if result:
        return result
    #=========================== REQUISIÇÕES =============================================================#
    dataSetor = apiResponse(request, f'http://{host}/prontocheck/setor/{idSetor}/', 'GET')
    datalocal = apiResponse(request, f'http://{host}/prontoticket/local/{local_id}/', 'GET')
    datalocal_2 = apiResponse(request, f'http://{host}/prontoticket/local/?setor={idSetor}', 'GET')
    dataItem = apiResponse(request, f'http://{host}/prontoticket/chkItem/?local_id={local_id}', 'GET')
    dataSubitem = apiResponse(request, f'http://{host}/prontoticket/chkSubIt/?setor_id={idSetor}', 'GET')
    dataSetorNome = apiResponse(request, f'http://{host}/prontocheck/setor/{idSetor}/', 'GET')
    #======================================================================================================#
    current_datetime = datetime.now()
    data_criacao = current_datetime.isoformat()
    dataAtual = current_datetime.strftime("%d/%m/%Y")
    print(dataAtual)

    i = 0
    x = 0
    if request.method == 'POST':
        for item in dataItem:
            if item['local_id'] == datalocal['id']:
                for SubItem in dataSubitem:
                    if SubItem['item_id'] == item['id']:
                        i += 1
                        SubItem_id  = SubItem["id"]
                        resposta = request.POST.get('pergunta{}'.format(SubItem_id))
                        descricao = request.POST.get('comentario{}'.format(SubItem_id))
                        evidencia = request.FILES.get('evidencia{}'.format(SubItem_id))
                        print(f'Pergunta: {SubItem["nome"]} <br> Resposta: {resposta}')
                        body_checklist = {
                            "criado_em": data_criacao,
                            "setor_id": idSetor,
                            "local_id": local_id,
                            "item_id": item['id'],
                            "subitem_id": SubItem['id']
                        }
                        #files["evidencia"] = evidencia
                        # Se tiver resposta vai ser salvo os dados
                        if resposta:
                            x += 1
                            body_checklist["resposta"] = resposta
                            files = {"evidencia": evidencia}
                            if descricao:
                                body_checklist["descricao"] = descricao
                            
                            pprint.pprint(body_checklist)
                            
                            pprint.pprint(files)
                            
                            resposta_checklist = apiResponse(request, f'http://{host}/prontoticket/checklist/', 'POST', data=body_checklist, file=files)
                            print(resposta_checklist)
                        print('========================================')
        print(f'Contagem:{i}')          
        print(f'Contagem 2:{x}')          
        #============ TRATATIVA PARA IR PRO PRÓXIMO LOCAL CASO O USUÁRIO ===============#
        proximoLocal = request.POST.get('prox_loc')
        if proximoLocal:
            print(f'O próximo local é: {proximoLocal}')
            return redirect(f'/prontocardio/prontoticket/checklist/{idSetor}/{proximoLocal}')
        else:
            return redirect(request.path)
        #=================================================================#
    context = {
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
        'setor': dataSetor,
        'localGeral': datalocal,
        'localSetor': datalocal_2,
        'itens': dataItem,
        'subitens': dataSubitem,
        'data':dataAtual,
    }
    return render(request, 'checklist/checklist.html', context)

def redirecCad(request):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')
    
    result = verifica_headers(request, headers)
    if result:
        return result

    dataSetor = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')
    dataLocal = apiResponse(request, f'http://{host}/prontoticket/local/', 'GET')
    

    if request.method == 'POST':
        localId = request.POST.get('local')
        setorId = request.POST.get('setor')
        return redirect(f'/prontocardio/prontoticket/cadastro/{setorId}')

    context = {
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
        'setores': dataSetor,
        'local': dataLocal,
    }
    return render(request, 'checklist/redirec_checklist.html', context)

def checklistCadastro(request, id_setor):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')

    result = verifica_headers(request, headers)
    if result:
        return result
    inicio = time.time()
    dataItem = apiResponse(request, f'http://{host}/prontoticket/chkItem/?setor_id={id_setor}', 'GET')
    dataSubitem = apiResponse(request, f'http://{host}/prontoticket/chkSubIt/?setor_id={id_setor}', 'GET')
    dataLocal = apiResponse(request, f'http://{host}/prontoticket/local/?setor={id_setor}', 'GET')
    dataSetor = apiResponse(request, f'http://{host}/setores/{id_setor}/', 'GET')

    #============================  MAPEAMENTOS =================================#
    mapeamento_itens = {item["id"]: item["nome"] for item in dataItem}  
    mapeamento_local = {item["id"]: item["local"] for item in dataLocal}  
    mapeamento_SubItem = {item["id"]: item["nome"] for item in dataSubitem}  
    mapeamento_SubItem = {item["id"]: item["nome"] for item in dataSubitem}  
    #===========================================================================#

    for item in dataSubitem:
        item["item_id"] = mapeamento_itens.get(item.get("item_id"))

    for item in dataItem:
        item["local_id"] = mapeamento_local.get(item.get("local_id"))

    pprint.pprint(dataSubitem)
    if request.method == 'POST':
        #Condições referentes a adição e edição de itens
        if '_method' in request.POST and request.POST['_method'] == 'D':
            item = request.POST['item']
            local_id = request.POST['itemLocalSelect']

            #print(f'esse é o novo item{item}, com o local {idLocal}')

            item_body = {
                "nome": item,
                "local_id": local_id,
                "setor_id": idSetor,
            }

            apiResponse(request, f'http://{host}/prontoticket/chkItem/', 'POST', data=item_body)
            return redirect(request.path)

        elif '_method' in request.POST and request.POST['_method'] == 'D_ALT':
            itemId = request.POST['idItem']
            novoMome = request.POST['novoNomeItem']
            local = int(request.POST['localSelect'])
            #print(f'esse é o novo nome do item {novoMome}, com o novo local {local}, nome antigo é {itemId}')

            item_body = {
                key: value for key, value in {
                    "nome": novoMome,
                    "local_id": local,
                }.items() if value != ''
            }

            apiResponse(request, f'http://{host}/prontoticket/chkItem/{itemId}/', 'PUT', data=item_body)

            return redirect(request.path)

        elif '_method' in request.POST and request.POST['_method'] == 'D_DEL':
            idItemDelete = request.POST.get('idItemDelete')

            apiResponse(request, f'http://{host}/prontoticket/chkItem/{idItemDelete}/', 'DEL')
            return redirect(request.path)

        #Condições referentes a adição e edição dos Subitens
        elif '_method' in request.POST and request.POST['_method'] == 'T':
            novoSubitem = request.POST.get('novoSubitem')
            itemSubitem = request.POST.get('itemSubitem')
            #print(f'esse é o novo item {novoSubitem}, e o item {itemSubitem}')

            subitem_body = {
                key: value for key, value in {
                    'nome': novoSubitem,
                    'item_id': itemSubitem,
                    'setor_id': idSetor,

                }.items() if value != ''
            }
            apiResponse(request, f'http://{host}/prontoticket/chkSubIt/', 'POST', data=subitem_body)
            return redirect(request.path)
        
        elif '_method' in request.POST and request.POST['_method'] == 'T_ALT':
            idSubitem = request.POST['idSubitem']
            novoNomeSubitem = request.POST.get('novoNomeSubitem')
            novoItem = int(request.POST.get('itemSelect'))
            #print(f'esse é o novo item {novoNomeSubitem}, com o novo item {novoItem} id novo subItem {idSubitem}')
            

            subitem_body = {
                key: value for key, value in {
                    'nome': novoNomeSubitem,
                    'item_id': novoItem,
                }.items() if value != ''
            }
            apiResponse(request, f'http://{host}/prontoticket/chkSubIt/{idSubitem}/', 'PUT', data=subitem_body)
            return redirect(request.path)

        elif '_method' in request.POST and request.POST['_method'] == 'T_DEL':
            idSubitemDelete = request.POST.get('idSubitemDelete')
            
            apiResponse(request, f'http://{host}/prontoticket/chkSubIt/{idSubitemDelete}/', 'DEL')
            return redirect(request.path)

        #Condições referentes a adição e edição dos Locais
        elif '_method' in request.POST and request.POST['_method'] == 'L':
            novoLocal = request.POST.get('novoLocal')

            local_body = {
                key: value for key, value in {
                    'local': novoLocal,
                    'setor': idSetor,
                }.items() if value != ''
            }
            apiResponse(request, f'http://{host}/prontoticket/local/', 'POST', data=local_body)
            return redirect(request.path)
        
        elif '_method' in request.POST and request.POST['_method'] == 'L_ALT':
            novoNomeLocal = request.POST.get('novoNomeLocal')
            idEditarLocal = request.POST.get('idLocal')
            #print(f'esse é o novo nome {novoNomeLocal}, com o id de {idEditarLocal}')

            local_body = {
                key: value for key, value in {
                    'local': novoNomeLocal,
                }.items() if value != ''
            }
            apiResponse(request, f'http://{host}/prontoticket/local/{idEditarLocal}/', 'PUT', data=local_body)
            return redirect(request.path)

        elif '_method' in request.POST and request.POST['_method'] == 'L_DEL':
            idlocalDelete = request.POST.get('idLocalDelete')

            apiResponse(request, f'http://{host}/prontoticket/local/{idlocalDelete}/', 'DEL')
            return redirect(request.path)

    context = {
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
        'itens': dataItem,
        'local': dataLocal,
        'setor': dataSetor,
        'subitens':dataSubitem,
    }
    fim = time.time()
    tempo_requisicao = fim - inicio

    print(tempo_requisicao)
    return render(request, 'checklist/checklist_cadastro.html', context)

def setorRelatorio(request):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')

    result = verifica_headers(request, headers)
    if result:
        return result

    dataset = apiResponse(request, f'{url_setores}', 'GET')

    if request.method == 'POST':
        setor = request.POST.get('setor')
        return redirect(f'/prontocardio/prontoticket/redireciona_relatorio/{setor}')

    context = {
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
        'setores': dataset,
    }
    return render(request, 'checklist/setor-relatorio.html', context)

def setorRelatorioPt2(request, idSetor):
    headers = request.session.get('headers')
    bloq_tela = request.session.get('id_setor')

    dataset = apiResponse(request, f'{url_setores}{idSetor}/', 'GET')
    data_checklist = apiResponse(request, f'{url_checklist}?setor_id={idSetor}', 'GET')
    result = consolidate_dates(data_checklist)

    if request.method == 'POST':
        data = request.POST.get('dataRelatorio')
        tipo_relatorio = request.POST.get('tp_rel')

        if tipo_relatorio == '1':
            print('Relatorio Consolidado')
            return redirect(f'/prontocardio/prontoticket/relatorio_v2/{idSetor}/{data}')
        if tipo_relatorio == '2':
            print('Relatorio Editavel')
            return redirect(f'/prontocardio/prontoticket/relatorio/{idSetor}/{data}')

    
    context = {
        'bloq_tela': bloq_tela,
        'nm_colaborador':request.session.get('nm_colaborador'),
        'setor':dataset,
        'datas':result,
    }
    return render(request, 'checklist/setor-relatorio-pt2.html', context)

def relatorioEditavel(request, idSetor, data):
    headers = request.session.get('headers')

    result = verifica_headers(request, headers)
    if result:
        return result
    #====================================================================================================#
    data_checklist = apiResponse(request, f'{url_checklist}?setor_id={idSetor}', 'GET')
    datalocal = apiResponse(request, f'http://{host}/prontoticket/local/?setor={idSetor}', 'GET')
    dataItem = apiResponse(request, f'http://{host}/prontoticket/chkItem/?setor_id={idSetor}', 'GET')
    dataSubitem = apiResponse(request, f'http://{host}/prontoticket/chkSubIt/?setor_id={idSetor}', 'GET')
    dataEvidenciasChecklist = apiResponse(request, f'http://{host}/prontoticket/checklistEvidencias/', 'GET')
    #====================================================================================================#
    filtered_data = filtrar_json_por_data(data_checklist, data)
    if request.method == 'POST':
        resposta = request.POST.get('resposta')
        comentario = request.POST.get('comentario')
        id_chklist = request.POST.get('id_chklist')
        evidencia = request.FILES.get('evidencia')
        print(evidencia)
        if '_method' in request.POST and request.POST['_method'] == 'DELETE':
            id_chklist = request.POST.get('id_chklist')
            dataDeleteChklist = apiResponse(request, f'{url_checklist}{id_chklist}/', 'DEL')
            return redirect(request.path)
        
        if '_method' in request.POST and request.POST['_method'] == 'EDITAR':
            print(f'o id da resposta é:{id_chklist}')
            imagem = request.FILES.get('arquivo')
            body_chklist = {}
            if resposta:
                body_chklist['resposta'] = resposta
            if comentario:
                body_chklist['descricao'] = comentario
            if evidencia is not None:
                files = {"evidencia": evidencia}
                print(files)
            else:
                files = None
            print(body_chklist)
            print('FUNÇÃO EDITAR')

            #dataEditarChklist = apiResponse(request, f'{url_checklist}{id_chklist}/', 'PUT',  files=files, data=body_chklist )
            response = requests.put(url=f"{url_checklist}{id_chklist}/", data=body_chklist, files=files, headers=headers)
            print(response)
            return redirect(request.path)
        
        if '_method' in request.POST and request.POST['_method'] == 'FOTOS':
            print('FUNÇÃO FOTO')
            id_resp = request.POST.get('id_resp')
            fotos_selecionadas = request.POST.getlist('fotos[]')

            for foto_id in fotos_selecionadas:
                # Enviar solicitação DELETE para a API para excluir a foto
                url_delete_foto = f'http://{host}/prontoticket/checklistEvidencias/{foto_id}/'  # Substitua pela URL correta da sua API
                responsedel = requests.delete(url=url_delete_foto, headers=headers)

                if responsedel.status_code == 204:
                    # A foto foi excluída com sucesso
                    print(f'Foto {foto_id} excluída com sucesso.')
                else:
                    # Ocorreu um erro ao excluir a foto, exibir a mensagem de erro
                    print(f'Falha ao excluir a foto {foto_id}. Erro: {responsedel.text}')

            files2 = request.FILES.getlist('evidencia')  # Obter a lista de arquivos enviados
            resposta_id = request.POST.get('id_resp')
            urlRespEvid = f'http://{host}/prontoticket/checklistEvidencias/'
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

            return redirect(request.path)
    
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'locais':datalocal,
        'itens':dataItem,
        'subitens':dataSubitem,
        'chklists':filtered_data,
        'data_esc':data,
        'nm_setor':apiResponse(request, f'{url_setores}{idSetor}/', 'GET'),
        'imagens':dataEvidenciasChecklist
    }
    return render(request, 'checklist/relatorio.html', context)

def relatorioConsolidado(request, idSetor, data):
    headers = request.session.get('headers')

    result = verifica_headers(request, headers)
    if result:
        return result
    #====================================================================================================#
    data_checklist = apiResponse(request, f'{url_checklist}?setor_id={idSetor}', 'GET')
    datalocal = apiResponse(request, f'http://{host}/prontoticket/local/?setor={idSetor}', 'GET')
    dataItem = apiResponse(request, f'http://{host}/prontoticket/chkItem/?setor_id={idSetor}', 'GET')
    dataSubitem = apiResponse(request, f'http://{host}/prontoticket/chkSubIt/?setor_id={idSetor}', 'GET')
    #====================================================================================================#

    filtered_data = filtrar_json_por_data(data_checklist, data)
    pprint.pprint(filtered_data)
    if request.method == 'POST':
        resposta = request.POST.get('resposta')
        comentario = request.POST.get('comentario')

        if '_method' in request.POST and request.POST['_method'] == 'DELETE':
            id_chklist = request.POST.get('id_chklist')
            dataDeleteChklist = apiResponse(request, f'{url_checklist}{id_chklist}/', 'DEL')
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'EDITAR':
            id_chklist = request.POST.get('id_chklist')
            body_chklist = {}
            if resposta is not None:
                body_chklist['resposta'] = resposta
            if comentario is not None  and comentario.strip() != '':
                body_chklist['descricao'] = comentario
            print(body_chklist)
            dataEditarChklist = apiResponse(request, f'{url_checklist}{id_chklist}/', 'PUT', data=body_chklist)
            print(f'resposta:{dataEditarChklist}')
            return redirect(request.path)
    
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'locais':datalocal,
        'itens':dataItem,
        'subitens':dataSubitem,
        'chklists':filtered_data,
        'data_esc':data,
        'nm_setor':apiResponse(request, f'{url_setores}{idSetor}/', 'GET')
    }
    return render(request, 'checklist/relatorio_V2.html', context)

#==========================================================================#
def filtroStatus(request):
    
    if request.method == 'POST':
        status = request.POST.get('status')
        coluna = request.POST.get('coluna')
        itensSelect = request.POST.get('itensSelect') 
        acesso = request.POST.get('acesso')
        bloq_tela = request.session.get('id_setor')
        groups = ', '.join(map(str, bloq_tela))
        
        if acesso == 'us':

            if itensSelect != '' and itensSelect != None and status != '':
                idUsuario = request.session.get('id_usuario')
                if status != 2:
                    chamado = apiResponse(request, f'http://{host}/prontoticket/chamados_pendentes/?{coluna}={itensSelect}&status={status}&usuario={idUsuario}', 'GET')
                else:
                    chamado = apiResponse(request, f'http://{host}/prontoticket/chamados/?{coluna}={itensSelect}&status={status}&usuario={idUsuario}', 'GET')
                
                return listarChamadoUsuario(request, chamado)
                
            elif itensSelect != '' and itensSelect != None:
                idUsuario = request.session.get('id_usuario')
                chamado = apiResponse(request, f'http://{host}/prontoticket/chamados_pendentes/?{coluna}={itensSelect}&usuario={idUsuario}', 'GET')
                return listarChamadoUsuario(request, chamado)

            elif status != '':
                idUsuario = request.session.get('id_usuario')
                chamado = apiResponse(request, f'http://{host}/prontoticket/chamados_pendentes/?status={status}&usuario={idUsuario}', 'GET')
                return listarChamadoUsuario(request, chamado)
            
            else:
                return redirect(f'/prontocardio/prontoticket/listar_chamado_usuario/')
        
        elif acesso == 'tec':

            if itensSelect != '' and itensSelect != None and status != '':
                idUsuario = request.session.get('id_usuario')
                if status != 2:
                    chamado = apiResponse(request, f'http://{host}/prontoticket/chamados_pendentes/?{coluna}={itensSelect}&status={status}&setor_recebe={groups}', 'GET')
                else:
                    chamado = apiResponse(request, f'http://{host}/prontoticket/chamados/?{coluna}={itensSelect}&status={status}&setor_recebe={groups}', 'GET')

                return listarChamado(request, chamado)
                
            elif itensSelect != '' and itensSelect != None:
                idUsuario = request.session.get('id_usuario')
                chamado = apiResponse(request, f'http://{host}/prontoticket/chamados_pendentes/?{coluna}={itensSelect}&setor_recebe={groups}', 'GET')
                return listarChamado(request, chamado)

            elif status != '':
                idUsuario = request.session.get('id_usuario')
                chamado = apiResponse(request, f'http://{host}/prontoticket/chamados_pendentes/?status={status}&setor_recebe={groups}', 'GET')
                return listarChamado(request, chamado)
            
            else:
                return redirect(f'/prontocardio/prontoticket/listar_chamado/')

#=============================INDICADOR BI ================================#
def indicadorBiTI(request):
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    }
    return render (request, 'indicador_bi.html', context)
#==========================================================================#