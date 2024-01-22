from django.shortcuts import render, redirect
from administrativo.views import host, apiResponse, render_error_404
import requests, json, pprint
from datetime import datetime

urlcli = f"http://{host}/nps/clinica/?created_at_year=2023"
urlemerg = f"http://{host}/nps/emergencia/?created_at_year=2023"
urlpos = f"http://{host}/nps/posalta/?created_at_year=2023"
urlPlayer = f"http://{host}/prontoplayer/videos/"
#===================NPS======================#

def npsClinica(request):
    headers = request.session.get('headers')
    if headers is None:
        return render_error_404(request)
    if request.method == 'POST':
        nomepaciente = request.POST.get('nomepaciente')
        convenio = request.POST.get('convenio')
        agilidade_recepcao = request.POST.get('agilidaderecepcao')
        atencao_recepcao = request.POST.get('atencaorecepcao')
        clareza_recepcao = request.POST.get('clarezarecepcao')
        enfermagem = request.POST.get('atendimentoenfermagem')
        medico = request.POST.get('atendimentomedico')
        localizacao = request.POST.get('localizacao')
        higienizacao = request.POST.get('higienizacao')
        estrutura = request.POST.get('estrutura')
        indicar = request.POST.get('indicacao') 
        encontrou = request.POST.get('encontrou') 
        comentario = request.POST.get('mensagem')
        
        user_data = {
            "nomepaciente": str(f"{nomepaciente}"),
            "convenio": str(f"{convenio}"),
            "agilidade_recepcao": f"{agilidade_recepcao}",
            "atencao_recepcao": f"{atencao_recepcao}",
            "clareza_recepcao": f"{clareza_recepcao}",
            "enfermagem": f"{enfermagem}",
            "medico": f"{medico}",
            "localizacao": f"{localizacao}",
            "higienizacao": f"{higienizacao}",
            "estrutura": f"{estrutura}",
            "indicar": str(f"{indicar}"),
            "encontrou": str(f"{encontrou}"),
            "comentario": str(f"{comentario}"),
        }

        response = requests.post(url=urlcli, json=user_data, headers=headers)
        data = response.json()
        print("clinica status: ", response.status_code)

        dataAbertura = data['created_at']
        dataCut = dataAbertura[:10]
        dataCut = dataCut.replace('-', '/')
        dataAbertura = dataCut[8:10] + dataCut[4:7] + dataCut[4] +  dataCut[0:4]
        
        context = {
            'resposta': user_data,
            'data': dataAbertura,
            'bloq_tela':request.session.get('id_setor'),
            'nm_colaborador':request.session.get('nm_colaborador'),
        }
        return render(request, 'formularios/finalizadocli.html', context)
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'values_range': range(11),
    }    
    return render(request, 'formularios/clinica.html', context)

def npsEmergencia(request):
    headers = request.session.get('headers')
    if headers is None:
        return render_error_404(request)
    urlEmerg = "http://192.168.4.33:8000/nps/emergencia/"

    if request.method == 'POST':
        nomepaciente = request.POST.get('nomepaciente')
        convenio = request.POST.get('convenio')
        agilidade_recepcao = request.POST.get('agilidade')
        atencao_recepcao = request.POST.get('atencao')
        clareza_recepcao = request.POST.get('clareza')
        enfermagem = request.POST.get('enfermagem')
        medico = request.POST.get('medico')
        localizacao = request.POST.get('localizacao')
        higienizacao = request.POST.get('higienizacao')
        estrutura = request.POST.get('estrutura')
        emergencia = request.POST.get('emergencia')
        indicar = request.POST.get('indicacao') 
        encontrou = request.POST.get('encontrou') 
        comentario = request.POST.get('mensagem')
        
        user_data = {
            "nomepaciente": f"{nomepaciente}",
            "convenio": f"{convenio}",
            "agilidade_recepcao": f"{agilidade_recepcao}",
            "atencao_recepcao": f"{atencao_recepcao}",
            "clareza_recepcao": f"{clareza_recepcao}",
            "enfermagem": f"{enfermagem}",
            "medico": f"{medico}",
            "localizacao": f"{localizacao}",
            "higienizacao": f"{higienizacao}",
            "estrutura": f"{estrutura}",
            "emergencia": f"{emergencia}",
            "indicar": str(f"{indicar}"),
            "encontrou": str(f"{encontrou}"),
            "comentario": f"{comentario}",
        }
        #pprint.pprint(user_data)
        response = requests.post(url=urlEmerg, json=user_data, headers= headers)
        data = response.json()

        if response.status_code <= 201:
            dataAbertura = data['created_at']
            dataCut = dataAbertura[:10]
            dataCut = dataCut.replace('-', '/')
            dataAbertura = dataCut[8:10] + dataCut[4:7] + dataCut[4] +  dataCut[0:4]
            
            context = {
                'resposta': user_data,
                'data': dataAbertura,
                'bloq_tela':request.session.get('id_setor'),
                'nm_colaborador':request.session.get('nm_colaborador'),
            }

            #pprint.pprint(data)
            pprint.pprint(response.status_code)
            return render(request, 'formularios/finalizadoemerg.html', context)

        
        else:
            print("status_emerg: ", response.status_code)
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'values_range': range(11),
    }   
    return render (request, 'formularios/emergencia.html', context)

def npsPosAlta(request):
    headers = request.session.get('headers')
    if headers is None:
        return render_error_404(request)
    url = "http://192.168.4.33:8000/nps/posalta/"
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'values_range': range(11),
    }
    if request.method == 'POST':
        nomepaciente = request.POST.get('nomepaciente')
        convenio = request.POST.get('convenio')
        unidadeinter = request.POST.get('unidadeinternacao')
        agilidade_enfermagem = request.POST.get('agilidadeenfermagem')
        atencao_enfermagem = request.POST.get('atencaoenfermagem')
        clareza_enfermagem = request.POST.get('clarezaenfermagem')
        atencao_medico = request.POST.get('atencaomedico')
        clareza_medico = request.POST.get('clarezamedico')
        nutricao = request.POST.get('nutricao')
        higienizacao = request.POST.get('higienizacao')
        estrutura = request.POST.get('estrutura')
        indicar = request.POST.get('indicacao') 
        encontrou = request.POST.get('encontrou') 
        comentario = request.POST.get('mensagem')  
        
        user_data = {
            "nomepaciente": f"{nomepaciente}",
            "convenio": f"{convenio}",
            "unidade_internacao": str(f"{unidadeinter}"),
            "agilidade_enfermagem": f"{agilidade_enfermagem}",
            "atencao_enfermagem": f"{atencao_enfermagem}",
            "clareza_enfermagem": f"{clareza_enfermagem}",
            "atencao_medico": f"{atencao_medico}",
            "clareza_medico": f"{clareza_medico}",
            "nutricao": f"{nutricao}",
            "higienizacao": f"{higienizacao}",
            "estrutura": f"{estrutura}",
            "encontrou": str(f"{encontrou}"),
            "indicar": str(f"{indicar}"),
            "comentario": f"{comentario}",
        }

        pprint.pprint(user_data['nomepaciente'])
        response = requests.post(url=url,json=user_data, headers= headers)
        data = response.json()
        pprint.pprint(data)

        if response.status_code <= 201:

            dataAbertura = data['created_at']
            dataCut = dataAbertura[:10]
            dataCut = dataCut.replace('-', '/')
            dataAbertura = dataCut[8:10] + dataCut[4:7] + dataCut[4] +  dataCut[0:4]
            
            context = {
                'resposta': user_data,
                'data': dataAbertura,
                'bloq_tela':request.session.get('id_setor'),
                'nm_colaborador':request.session.get('nm_colaborador'),
            }
            pprint.pprint(response.status_code)
            return render(request, 'formularios/finalizadoemerg.html', context)

                
        else:
            print("status_posAlt: ", response.status_code)

        return render(request, 'finalizadoposalta.html')
    return render (request, 'formularios/posalta.html', context)

def listagem(request, id_esc):
    headers = request.session.get('headers')
    if headers is None:
        return render_error_404(request)
    
    if id_esc == 1:
        id_esc = 'Clínica'
        response = requests.get(url=urlcli, headers=headers)
        data = response.json()
        pprint.pprint(data)
        context = {
            'dados':data,
            'nome': id_esc,
            'bloq_tela':request.session.get('id_setor'),
            'nm_colaborador':request.session.get('nm_colaborador'),
        }
        return render(request, 'lista-nps.html', context)
    
    elif id_esc == 2:
        id_esc = 'Emergência'
        response = requests.get(url=urlemerg, headers=headers)
        data = response.json()

        for item in data:
            dataAbertura = str(item['created_at'])
            dataAlteracao = str(item['updated_at'])
            
            dataCut = dataAbertura[:10]
            dataCut = dataCut.replace('-', '/')

            dataAbertura = dataCut[8:10] + dataCut[4:7] + dataCut[4] +  dataCut[0:4]
            
            item['created_at'] = dataAbertura

        context = {
            'dados':data,
            'nome': id_esc,
            'bloq_tela':request.session.get('id_setor'),
            'nm_colaborador':request.session.get('nm_colaborador'),
        }
        return render(request, 'lista-nps.html', context)
    
    else:
        id_esc = 'Pós-Alta'
        response = requests.get(url=urlpos, headers=headers)
        data = response.json()
        
        for item in data:
            dataAbertura = str(item['created_at'])
            dataAlteracao = str(item['updated_at'])
            
            dataCut = dataAbertura[:10]
            dataCut = dataCut.replace('-', '/')

            dataAbertura = dataCut[8:10] + dataCut[4:7] + dataCut[4] +  dataCut[0:4]
            
            item['created_at'] = dataAbertura

        context = {
            'dados':data,
            'nome': id_esc,
            'bloq_tela':request.session.get('id_setor'),
            'nm_colaborador':request.session.get('nm_colaborador'),
        }
        return render(request, 'lista-nps.html', context)
    return render (request, 'lista-nps.html')

def formularios(request):
    headers = request.session.get('headers')
    if headers is None:
        return render_error_404(request)
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    }
    return render (request, 'formularios/formularios.html', context)

def dashboardnps(request):
    headers = request.session.get('headers')
    if headers is None:
        return render_error_404(request)
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    }
    return render(request, 'dashboardnps.html', context)

def prontoPlayer(request):
    headers = request.session.get('headers')
    if headers is None:
        return render_error_404(request)

    dataVideo = apiResponse(request,urlPlayer, 'GET')

    for item in dataVideo:
        dataAbertura = item['create_at']
        dataAbertura = dataAbertura[0:10]
        item['create_at'] = dataAbertura

        dataAbertura = item['create_at']
        data_objeto = datetime.fromisoformat(dataAbertura)
        data_formatada = data_objeto.strftime("%d-%m-%Y")
        item['create_at'] = data_formatada
        mes_da_resposta = item['create_at'][:10]
        item['create_at'] = mes_da_resposta
    
    if request.method == 'POST':
        if '_method' in request.POST and request.POST['_method'] == 'ADD':
            titulo = request.POST.get('titulo')
            descrição = request.POST.get('comentario')
            video = request.FILES.get('video')
            files = {"file": video}
            body = {
                "title": titulo,
                "description": descrição,
            }
            print(body)
            dataPlayer = apiResponse(request, urlPlayer, 'POST', data=body, file=files)
            print(dataPlayer)
            return redirect('prontoPlayer')
        elif '_method' in request.POST and request.POST['_method'] == 'DEL':
            video_id = request.POST.get('id_video')
            urlPlayer_id = (f'{urlPlayer}{video_id}/')
            dataPlayerDel = apiResponse(request, urlPlayer_id, 'DEL')
            print(dataPlayerDel)
            return redirect('prontoPlayer')


    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'video_list':dataVideo
    }
    return render(request, 'prontoplayer.html', context)

