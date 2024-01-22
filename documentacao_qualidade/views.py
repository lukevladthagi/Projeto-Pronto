from django.shortcuts import render, redirect
from administrativo.views import *
import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta

pastas = f"http://{host}/documentacao_qualidade/cadastro-pasta/"
arquivos = f"http://{host}/documentacao_qualidade/cadastro-documento/"
tp_documento = f"http://{host}/documentacao_qualidade/tipo-documento/"
setor_sigla = f"http://{host}/documentacao_qualidade/setor-sigla/"
setor = f"http://{host}/setores/"
usuarios = f"http://{host}/usuarios/"
central_solicitacao = f"http://{host}/documentacao_qualidade/central-solicitacao/"
central_solicitacao_status = f"http://{host}/documentacao_qualidade/central-solicitacao-status/"
central_solicitacao_tipo_timeline = f"http://{host}/documentacao_qualidade/central-solicitacao-tipo-timeline/"
central_solicitacao_timeline = f"http://{host}/documentacao_qualidade/central-solicitacao-timeline/"

#=============================== PASTAS COMPARTILHADAS =================================#

def pastas_documentacao(request):
    setor_ids = request.session.get('id_setor')
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
    #================== ARQUIVOS JSONS ==========================#
    params = "&".join(f"setor={id}" for id in setor_ids)
    print(f'{pastas}?{params}')
    data_pasta = apiResponse(request,f'{pastas}?{params}', 'GET' )
    data_setor = apiResponse(request,setor, 'GET' )
    #============================================================#
    for pasta in data_pasta:
        # Converter para objeto datetime
        data_created = datetime.strptime(pasta['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
    #================== ARQUIVOS JSONS ==========================#
    #================== ALTERAÇÕES ID'S POR NOMES ==========================#
    
    # Formatar como dia-mes-ano
    pasta['created_at'] = data_created.strftime("%d-%m-%Y")

    lista_ids  = pasta['setor']
    
    # Criar um dicionário para mapear IDs para nomes de setores
    mapeamento_ids_nomes = {setor['id']: setor['name'] for setor in data_setor}

    # Substituir os IDs pelos nomes dos setores na lista original
    lista_nomes_setores = [mapeamento_ids_nomes[id] for id in lista_ids]
    
    pasta['setor'] = lista_nomes_setores    
    
    
    #=====================================================================#
    
    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'REN_PASTA':
            nv_nm_pasta = request.POST.get('novo_nome_pasta')
            id_pasta = request.POST.get('id_pasta')
            descricao_pasta = request.POST.get('descricao_pasta')
            id_setor = request.POST.getlist('setores[]')
            body_pasta = {}
            if nv_nm_pasta:
                body_pasta['nome'] = nv_nm_pasta
            if descricao_pasta:
                body_pasta['descricao'] = descricao_pasta
            if id_setor:
                body_pasta['setor'] = id_setor
            print(f'O body enviado:{body_pasta}')
            print(100*'=')
            #=============== URL C/ ID DA PASTA ================#
            data_pasta_pt2 = apiResponse(request,f'{pastas}{id_pasta}/', 'GET' )
            data_resp = apiResponse(request, f'{pastas}{id_pasta}/', 'PUT', data=body_pasta)
            #===================================================#
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'NV_PASTA':
            nome_pasta = request.POST.get('nome_pasta')
            descricao_pasta = request.POST.get('descricao_pasta')
            id_setor = request.POST.getlist('setores[]')
            body_pasta = {
                "nome": {nome_pasta},
                "descricao": {descricao_pasta},
                "setor": id_setor
            }
            pprint.pprint(body_pasta)
            data_resp = apiResponse(request, pastas, 'POST', data=body_pasta)
            return redirect(request.path)
        
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'pastas':data_pasta,
        'setores':data_setor,
        'qt_pasta':len(data_pasta),
    }    
    #==========================================================================#
    #setores_filtrados = [setor for setor in data_setor if setor['id'] in context['bloq_tela']]
    pprint.pprint(context['bloq_tela'])
    print(100*"=")
    pprint.pprint(data_pasta)
    #print(100*"=")
    #ids_filtrados = [item1['id'] for item1 in data_pasta for item2 in setores_filtrados if set(item1['setor']) & set([item2['name']])]
    #print(100*"=")
    #pprint.pprint(f'{ids_filtrados} Oi')
    
    #context['setores_filtrados'] = setores_filtrados
    #==========================================================================#               
            
    return render(request, 'documentos_publicos/documentos_publicos.html', context)

def pastas_arquivo_documentacao(request,id_pasta):
    setor_ids = request.session.get('id_setor')
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
    #================== ARQUIVOS JSONS ==========================#
    data_pasta = apiResponse(request,f'{pastas}{id_pasta}/', 'GET' )
    data_arquivo = apiResponse(request,f'{arquivos}?pasta={id_pasta}&compartilhado=true', 'GET' )
    data_tp_doc = apiResponse(request,tp_documento, 'GET' )
    data_setor = apiResponse(request,setor, 'GET' )
    #============================================================#
    print(f'{arquivos}?pasta={id_pasta}')

    # Obter a quantidade total de itens
    quantidade_total_arq = len(data_arquivo)
    quantidade_total = len(data_arquivo)
    quantidade_total += 1
    quantidade_formatada = str(quantidade_total).zfill(3)
    # Imprimir o resultado
    #print(f"A quantidade total de itens na lista é: {quantidade_formatada}")
    #print('Aqui mah')
    #============================================================#
    for doc in data_arquivo:
        # Converter para objeto datetime
        data_created = datetime.strptime(doc['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        data_update = datetime.strptime(doc['updated_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        data_emissao = datetime.strptime(doc['data_emissao'], "%Y-%m-%d")
        data_prx_rev = datetime.strptime(doc['prox_revisao'], "%Y-%m-%d")

        # Formatar como dia-mes-ano
        doc['created_at'] = data_created.strftime("%d-%m-%Y")
        doc['updated_at'] = data_update.strftime("%d-%m-%Y")
        doc['data_emissao'] = data_emissao.strftime("%d-%m-%Y")
        doc['prox_revisao'] = data_prx_rev.strftime("%d-%m-%Y")
        for setores in data_setor:
            if doc['setor'] == setores['id']:
                doc['setor'] = setores['name']

    #============================================================#
    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'CAD_DOC':
            descricao_pasta = request.POST.get('descricao_pasta')
            data_criacao = request.POST.get('data_criacao')
            id_setor = request.POST.get('setor')
            tipo_documento = request.POST.get('tipo_documento')
            documento = request.FILES.get('arquivos')
            #========================== PEGANDO AS SIGLAS ==========================#
            data_set_sig = apiResponse(request,f'{setor_sigla}?setor={id_setor}', 'GET' )
            nm_set = data_set_sig[0]['sigla']
            
            data_tp_doc = apiResponse(request,f'{tp_documento}{tipo_documento}/', 'GET' )
            nm_tp_doc = data_tp_doc['sigla']
            nm_tp_doc = nm_tp_doc.upper()
            validade_tp_doc = data_tp_doc['validade']
            print(100*'=')
            # Convertendo a string para um objeto datetime
            data_inicial = datetime.strptime(data_criacao, '%Y-%m-%d')

            # Adicionando a quantidade de anos desejada, considerando anos bissextos
            nova_data = data_inicial + relativedelta(years=validade_tp_doc)

            # Convertendo o resultado de volta para uma string
            nova_data_str = nova_data.strftime('%Y-%m-%d')

            # Exibindo a nova data como string
            print(nova_data_str)
            print(100*'=')
            
            #=======================================================================#
            # nm_tp_doc é a sigla do doc
            # nm_set é a sigla do setor
            body_doc = {
                "codigo": f'{nm_tp_doc}.{nm_set}{quantidade_formatada}',
                "descricao": f'{descricao_pasta}',
                "data_emissao": f'{data_criacao}',
                "prox_revisao": f'{nova_data_str}',
                "pasta": f'{id_pasta}',
                "setor": f'{id_setor}',
                "tipo_documento": f'{tipo_documento}',
                "responsavel": request.session.get('id_usuario')
            }
            if documento is not None:
                files = {"arquivo": documento}
            dataresposta = apiResponse(request, arquivos, 'POST', data=body_doc, file=files)
            print(dataresposta)
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'REV_DOC':
            id_doc = request.POST.get('id_doc')
            descricao_pasta = request.POST.get('descricao_pasta')
            data_criacao = request.POST.get('data_criacao')
            compartilhado = request.POST.get('compartilhado')
            documento = request.FILES.get('arquivos')
            print(documento)
            if compartilhado is None:
                compartilhado = False
            #====================== VERSIONAMENTO DO DOC ==================#
            data_doc = apiResponse(request,f'{arquivos}{id_doc}/', 'GET' )
            tipo_documento = data_doc['tipo_documento']
            #==============================================================#
            #========================== PEGANDO AS SIGLAS ==========================#      
                  
            data_tp_doc = apiResponse(request,f'{tp_documento}{tipo_documento}/', 'GET' )
            validade_tp_doc = data_tp_doc['validade']
            #Convertendo a string para um objeto datetime
            data_inicial = datetime.strptime(data_criacao, '%Y-%m-%d')

            # Adicionando a quantidade de anos desejada, considerando anos bissextos
            nova_data = data_inicial + relativedelta(years=validade_tp_doc)

            # Convertendo o resultado de volta para uma string
            nova_data_str = nova_data.strftime('%Y-%m-%d')

            # Exibindo a nova data como string
            print(nova_data_str)

            
            #=======================================================================#
            body_doc = {
                "descricao": f'{descricao_pasta}',
                "data_emissao": f'{data_criacao}',
                "prox_revisao":f'{nova_data_str}',
                "responsavel": request.session.get('id_usuario'),   
            }
            body_doc['versao'] = data_doc['versao'] + 1
            if documento is not None:
                files = {"arquivo": documento}
            data_arquivo = apiResponse(request, f'{arquivos}{id_doc}/', 'PUT', data=body_doc,file=files)
            pprint.pprint(body_doc)
            pprint.pprint(files)
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'LIBERACAO':
            id_doc = request.POST.get('id_doc')
            compartilhado = True
            body_doc = {
                "compartilhado": f'{compartilhado}', 
            }
            data_arquivo = apiResponse(request, f'{arquivos}{id_doc}/', 'PUT', data=body_doc)
            print(data_arquivo)
            print('LIBERAÇÃO')
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'EXCLUIR':
            print('Vai esxcluir este documento')
            return redirect(request.path)


        
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'pastas':data_pasta,
        'arquivos':data_arquivo,
        'tp_docs':data_tp_doc,
        'setores':data_setor,
        'qt_arq':quantidade_total_arq,
    }    
    return render(request, 'documentos_publicos/arquivos_publicos.html', context)

#============================== LISTA MESTRA =======================#
def cadastro_pasta(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
    #================== ARQUIVOS JSONS ==========================#
    data_pasta = apiResponse(request,pastas, 'GET' )
    data_setor = apiResponse(request,setor, 'GET' )
    #================== ARQUIVOS JSONS ==========================#
    for pasta in data_pasta:
        # Converter para objeto datetime
        data_created = datetime.strptime(pasta['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # Formatar como dia-mes-ano
        pasta['created_at'] = data_created.strftime("%d-%m-%Y")

        lista_ids  = pasta['setor']
        
        # Criar um dicionário para mapear IDs para nomes de setores
        mapeamento_ids_nomes = {setor['id']: setor['name'] for setor in data_setor}

        # Substituir os IDs pelos nomes dos setores na lista original
        lista_nomes_setores = [mapeamento_ids_nomes[id] for id in lista_ids]
        
        pasta['setor'] = lista_nomes_setores    
    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'REN_PASTA':
            nv_nm_pasta = request.POST.get('novo_nome_pasta')
            id_pasta = request.POST.get('id_pasta')
            descricao_pasta = request.POST.get('descricao_pasta')
            id_setor = request.POST.getlist('setores[]')
            body_pasta = {}
            if nv_nm_pasta:
                body_pasta['nome'] = nv_nm_pasta
            if descricao_pasta:
                body_pasta['descricao'] = descricao_pasta
            if id_setor:
                body_pasta['setor'] = id_setor
            print(f'O body enviado:{body_pasta}')
            print(100*'=')
            #=============== URL C/ ID DA PASTA ================#
            data_pasta_pt2 = apiResponse(request,f'{pastas}{id_pasta}/', 'GET' )
            data_resp = apiResponse(request, f'{pastas}{id_pasta}/', 'PUT', data=body_pasta)
            #===================================================#
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'NV_PASTA':
            nome_pasta = request.POST.get('nome_pasta')
            descricao_pasta = request.POST.get('descricao_pasta')
            id_setor = request.POST.getlist('setores[]')
            body_pasta = {
                "nome": {nome_pasta},
                "descricao": {descricao_pasta},
                "setor": id_setor
            }
            pprint.pprint(body_pasta)
            data_resp = apiResponse(request, pastas, 'POST', data=body_pasta)
            return redirect(request.path)
        
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'pastas':data_pasta,
        'setores':data_setor,
        'qt_pasta':len(data_pasta)
    }    
    
    return render(request, 'cadastro_de_pasta.html', context)

def cadastro_arquivos_pastas(request,id_pasta):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
    #================== ARQUIVOS JSONS ==========================#
    data_pasta = apiResponse(request,f'{pastas}{id_pasta}/', 'GET' )
    data_arquivo = apiResponse(request,f'{arquivos}?pasta={id_pasta}', 'GET' )
    data_tp_doc = apiResponse(request,tp_documento, 'GET' )
    data_setor = apiResponse(request,setor, 'GET' )
    #============================================================#

    # Obter a quantidade total de itens
    quantidade_total_arq = len(data_arquivo)
    quantidade_total = len(data_arquivo)
    quantidade_total += 1
    quantidade_formatada = str(quantidade_total).zfill(3)
    # Imprimir o resultado
    #print(f"A quantidade total de itens na lista é: {quantidade_formatada}")
    #print('Aqui mah')
    #============================================================#
    for doc in data_arquivo:
        # Converter para objeto datetime
        data_created = datetime.strptime(doc['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        data_update = datetime.strptime(doc['updated_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        data_emissao = datetime.strptime(doc['data_emissao'], "%Y-%m-%d")
        data_prx_rev = datetime.strptime(doc['prox_revisao'], "%Y-%m-%d")

        # Formatar como dia-mes-ano
        doc['created_at'] = data_created.strftime("%d-%m-%Y")
        doc['updated_at'] = data_update.strftime("%d-%m-%Y")
        doc['data_emissao'] = data_emissao.strftime("%d-%m-%Y")
        doc['prox_revisao'] = data_prx_rev.strftime("%d-%m-%Y")
        for setores in data_setor:
            if doc['setor'] == setores['id']:
                doc['setor'] = setores['name']

    #============================================================#
    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'CAD_DOC':
            descricao_pasta = request.POST.get('descricao_pasta')
            data_criacao = request.POST.get('data_criacao')
            id_setor = request.POST.get('setor')
            tipo_documento = request.POST.get('tipo_documento')
            documento = request.FILES.get('arquivos')
            #========================== PEGANDO AS SIGLAS ==========================#
            data_set_sig = apiResponse(request,f'{setor_sigla}?setor={id_setor}', 'GET' )
            nm_set = data_set_sig[0]['sigla']
            
            data_tp_doc = apiResponse(request,f'{tp_documento}{tipo_documento}/', 'GET' )
            nm_tp_doc = data_tp_doc['sigla']
            nm_tp_doc = nm_tp_doc.upper()
            validade_tp_doc = data_tp_doc['validade']
            print(100*'=')
            # Convertendo a string para um objeto datetime
            data_inicial = datetime.strptime(data_criacao, '%Y-%m-%d')

            # Adicionando a quantidade de anos desejada, considerando anos bissextos
            nova_data = data_inicial + relativedelta(years=validade_tp_doc)

            # Convertendo o resultado de volta para uma string
            nova_data_str = nova_data.strftime('%Y-%m-%d')

            # Exibindo a nova data como string
            print(nova_data_str)
            print(100*'=')
            
            #=======================================================================#
            # nm_tp_doc é a sigla do doc
            # nm_set é a sigla do setor
            body_doc = {
                "codigo": f'{nm_tp_doc}.{nm_set}{quantidade_formatada}',
                "descricao": f'{descricao_pasta}',
                "data_emissao": f'{data_criacao}',
                "prox_revisao": f'{nova_data_str}',
                "pasta": f'{id_pasta}',
                "setor": f'{id_setor}',
                "tipo_documento": f'{tipo_documento}',
                "responsavel": request.session.get('id_usuario')
            }
            if documento is not None:
                files = {"arquivo": documento}
            dataresposta = apiResponse(request, arquivos, 'POST', data=body_doc, file=files)
            print(dataresposta)
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'REV_DOC':
            id_doc = request.POST.get('id_doc')
            descricao_pasta = request.POST.get('descricao_pasta')
            data_criacao = request.POST.get('data_criacao')
            compartilhado = request.POST.get('compartilhado')
            documento = request.FILES.get('arquivos')
            print(documento)
            if compartilhado is None:
                compartilhado = False
            #====================== VERSIONAMENTO DO DOC ==================#
            data_doc = apiResponse(request,f'{arquivos}{id_doc}/', 'GET' )
            tipo_documento = data_doc['tipo_documento']
            #==============================================================#
            #========================== PEGANDO AS SIGLAS ==========================#      
                  
            data_tp_doc = apiResponse(request,f'{tp_documento}{tipo_documento}/', 'GET' )
            validade_tp_doc = data_tp_doc['validade']
            #Convertendo a string para um objeto datetime
            data_inicial = datetime.strptime(data_criacao, '%Y-%m-%d')

            # Adicionando a quantidade de anos desejada, considerando anos bissextos
            nova_data = data_inicial + relativedelta(years=validade_tp_doc)

            # Convertendo o resultado de volta para uma string
            nova_data_str = nova_data.strftime('%Y-%m-%d')

            # Exibindo a nova data como string
            print(nova_data_str)

            
            #=======================================================================#
            body_doc = {
                "descricao": f'{descricao_pasta}',
                "data_emissao": f'{data_criacao}',
                "prox_revisao":f'{nova_data_str}',
                "responsavel": request.session.get('id_usuario'),   
            }
            body_doc['versao'] = data_doc['versao'] + 1
            if documento is not None:
                files = {"arquivo": documento}
            data_arquivo = apiResponse(request, f'{arquivos}{id_doc}/', 'PUT', data=body_doc,file=files)
            pprint.pprint(body_doc)
            pprint.pprint(files)
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'LIBERACAO':
            id_doc = request.POST.get('id_doc')
            compartilhado = True
            body_doc = {
                "compartilhado": f'{compartilhado}', 
            }
            data_arquivo = apiResponse(request, f'{arquivos}{id_doc}/', 'PUT', data=body_doc)
            print(data_arquivo)
            print('LIBERAÇÃO')
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'EXCLUIR':
            print('Vai esxcluir este documento')
            return redirect(request.path)


        
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'pastas':data_pasta,
        'arquivos':data_arquivo,
        'tp_docs':data_tp_doc,
        'setores':data_setor,
        'qt_arq':quantidade_total_arq,
    }    
    return render(request, 'arquivo_pasta.html', context)
#===================================================================#

#============================== CADASTROS EM GERAL ===================#
def cadastro_tipo_documento(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    #================== ARQUIVOS JSONS ==========================#
    data_tp_doc = apiResponse(request,tp_documento, 'GET' )
    #================== ARQUIVOS JSONS ==========================#
    
    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'EDITAR_TP_DOC':
            id_tp_doc = request.POST.get('id_tp_doc')
            nome_doc = request.POST.get('nome_doc')
            sigla_doc = request.POST.get('sigla_doc')
            validade_doc = request.POST.get('validade_doc')
            print(f'{nome_doc} - {sigla_doc}')
            #================== EDITAR na API ==========================#
            body_tp_doc = {}
            if nome_doc:
                body_tp_doc["nome"] = f"{nome_doc}"
            if sigla_doc:
                body_tp_doc["sigla"] = f"{sigla_doc}"
            if validade_doc:
                body_tp_doc["validade"] = int(validade_doc)
            print(80*'=')
            print(body_tp_doc) 
            data_tp_doc = apiResponse(request,f'{tp_documento}{id_tp_doc}/','PUT', data=body_tp_doc)
            print(data_tp_doc) 
            
            #===========================================================#
            return redirect(request.path)
            
        if '_method' in request.POST and request.POST['_method'] == 'DELETAR_TP_DOC':
            id_tp_doc = request.POST.get('id_tp_doc')
            print(20*'=')
            print(f'id do tipo de documento:{id_tp_doc}')
            #================== excluir na API ==========================#
            data_tp_doc = apiResponse(request,f'{tp_documento}{id_tp_doc}/','DEL')
            #===========================================================#
            return redirect(request.path)
        
        if '_method' in request.POST and request.POST['_method'] == 'ADD_TP_DOC':
            nome_doc = request.POST.get('nome_doc')
            sigla_doc = request.POST.get('sigla_doc')
            validade_doc = request.POST.get('validade_doc')
            #================== SALVAR na API ==========================#
            body_tp_doc = {}
            if nome_doc:
                body_tp_doc["nome"] = f"{nome_doc}"
            if sigla_doc:
                body_tp_doc["sigla"] = f"{sigla_doc}"
            if validade_doc:
                body_tp_doc["validade"] = int(validade_doc)
            print(80*'=')
            print(body_tp_doc)    
            data_tp_doc = apiResponse(request,tp_documento,'POST', data=body_tp_doc)
            pprint.pprint(data_tp_doc)
            #===========================================================#
            return redirect(request.path)
        
        
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'tp_doc':data_tp_doc,
    }  
    return render(request, 'cadastros/cadastro_tipo_documento.html',context)

def cadastro_geral(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
    if request.method == "POST":
        tp_cadastro = request.POST.get('tp_cadastro')
        print(tp_cadastro)
        if tp_cadastro == 'tp_doc':
            return redirect(f'/prontocardio/documentacao_qualidade/cadastro-tipo-documento')
        if tp_cadastro == 'doc_sigla':
            return redirect(f'/prontocardio/documentacao_qualidade/cadastro-documento-sigla')
        if tp_cadastro == 'venc_doc':
            return redirect(f'/prontocardio/documentacao_qualidade/cadastro-vencimento-documento')
        if tp_cadastro == 'setor_sigla':
            return redirect(f'/prontocardio/documentacao_qualidade/cadastro-setor-sigla')
    
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    }  
    return render(request, 'cadastros/cadastro_geral.html',context)

def cadastro_setor_sigla(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'ADD_SET_SIG':
            id_Set = request.POST.get('id_Set')
            sigla_set = request.POST.get('sigla_set')
            #================== SALVAR na API ==========================#
            body_set_sig = {}
            if id_Set:
                body_set_sig["setor"] = {id_Set}
            if sigla_set:
                body_set_sig["sigla"] = f"{sigla_set}"
            data_tp_doc = apiResponse(request,setor_sigla,'POST', data=body_set_sig)
            print(100*'=')
            print(data_tp_doc)
            #===========================================================#
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'EDITAR_SET_SIGLA':
            id_set_sigla = request.POST.get('id_set_sigla')
            sigla_set = request.POST.get('sigla_set')
            #================== EDITAR na API ==========================#
            body_set_sig = {}
            if sigla_set:
                body_set_sig["sigla"] = {sigla_set}
            data_tp_doc = apiResponse(request,f'{setor_sigla}{id_set_sigla}/','PUT', data=body_set_sig)
            #===========================================================#
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'DELET_SET_SIGLA':
            id_set_sigla = request.POST.get('id_set_sigla')
            #================== EXCLUIR na API ==========================#
            data_tp_doc = apiResponse(request,f'{setor_sigla}{id_set_sigla}/','DEL')
            print(data_tp_doc)
            #===========================================================#
            return redirect(request.path)
        
        
    #================== ARQUIVOS JSONS ==========================#
    data_set_sigla = apiResponse(request,setor_sigla, 'GET' )
    data_setor = apiResponse(request,setor, 'GET' )
    #================== ARQUIVOS JSONS ==========================#
    
    for setSigla in data_set_sigla:
        for setor2 in data_setor:
            if setSigla['setor'] == setor2['id']:
                setSigla['setor'] = setor2['name']
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'set_sigla':data_set_sigla,
        'setores':data_setor,
    }  
    return render (request, 'cadastros/cadastro_setor_sigla.html', context)
#====================================================================#

def central_qualidade(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
    #================== ARQUIVOS JSONS ==========================#
    data_cent_sol = apiResponse(request,central_solicitacao, 'GET' )
    data_cent_sol_status = apiResponse(request,central_solicitacao_status, 'GET' )
    data_setor = apiResponse(request,setor, 'GET' )
    data_tp_doc = apiResponse(request,tp_documento, 'GET' )
    #================== ARQUIVOS JSONS ==========================#
    
    #================== TROCA ID'S POR NOME =====================#
    for solicitacoes in data_cent_sol:
        for status in data_cent_sol_status:
            if solicitacoes['status'] == status['id']:
                solicitacoes['status'] = status['status']
        for tp_doc in data_tp_doc:
            if solicitacoes['tipo_documento'] == tp_doc['id']:
                solicitacoes['tipo_documento'] = tp_doc['nome']
    #============================================================#
    
    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'SOL_PAD':
            nome_documento = request.POST.get('nm_doc')
            descricao_ajustes = request.POST.get('desc_doc')
            setor_esc = request.POST.get('setor')
            tipo_documento = request.POST.get('tp_doc')
            documento = request.FILES.get('documento')
            
            
            body_sol_doc = {
                "nm_doc": nome_documento,
                "comentario": descricao_ajustes,
                "tipo_documento": tipo_documento,
                "setor": setor_esc,
                "solicitante": request.session.get('id_usuario')
            }
            if documento is not None:
                files = {"arquivo": documento}
            
            data_arquivo = apiResponse(request, central_solicitacao, 'POST', data=body_sol_doc,file=files)
            
            body_timeline = {
                "comentario": "Abertura de Solicitação",
                "solicitacao": data_arquivo['id'],
                "usuario": request.session.get('id_usuario'),
                "tipo": 1
            }
            data_arquivo = apiResponse(request, central_solicitacao_timeline, 'POST', data=body_timeline)
            
            pprint.pprint(body_sol_doc)
            pprint.pprint(data_arquivo)
            return redirect(request.path)
            

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'solicitacoes':data_cent_sol,
        'setores':data_setor,
        'tp_docs':data_tp_doc,
    } 
    return render (request, 'central/central_qualidade.html', context)

def central_qualidade_solicitacao(request,id_solicitacao):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
   
    #================== ARQUIVOS JSONS ==========================#
    data_cent_sol = apiResponse(request,f'{central_solicitacao}{id_solicitacao}/', 'GET' )
    data_cent_sol_tp_timeline = apiResponse(request,central_solicitacao_tipo_timeline, 'GET' )
    data_cent_sol_timeline = apiResponse(request,f'{central_solicitacao_timeline}?solicitacao={id_solicitacao}', 'GET' )
    data_usuarios = apiResponse(request,usuarios, 'GET' )
    #================== ARQUIVOS JSONS ==========================#
    pprint.pprint(data_cent_sol)
    for timeline in data_cent_sol_timeline:
        #============================== AJUSTE DE DATA ==================================#
        data_objeto = datetime.strptime(timeline['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # Formatar a data para "07/01/2024" e a hora para "11:36"
        timeline['created_at'] = data_objeto.strftime("%d/%m/%Y às %H:%M")
        #================================================================================#

        #============================== TROCA DE ID'S ===================================#        
        for tp_timeline in data_cent_sol_tp_timeline:
            if timeline['tipo'] == tp_timeline['id']:
                timeline['icone'] = tp_timeline['icone']
                timeline['tp_requisicao'] = tp_timeline['descricao']
        for usuario in data_usuarios:
            if timeline['usuario'] == usuario['id']:
                timeline['usuario'] = usuario['nome']
        # URL que você deseja renderizar dentro do seu template
    
    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'INCLUSAO':
            descricao = request.POST.get('descricao')
            documento = request.FILES.get('documento')
            body_timeline = {
                "comentario": descricao,
                "solicitacao": id_solicitacao,
                "usuario": request.session.get('id_usuario'),
                "tipo": 9
            }
            if documento is not None:
                files = {"arquivo": documento}
            data_arquivo = apiResponse(request, central_solicitacao_timeline, 'POST', data=body_timeline,file=files)
            print(data_arquivo)
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'APROV':
            descricao = request.POST.get('descricao')

            body_timeline = {
                "comentario": descricao,
                "solicitacao": id_solicitacao,
                "usuario": request.session.get('id_usuario'),
                "tipo":11
            }
            body_solicitacao= {
                "status": 2
            }
            data_arquivo = apiResponse(request, central_solicitacao_timeline, 'POST', data=body_timeline)
            data_arquivo2 = apiResponse(request, f'{central_solicitacao}{id_solicitacao}/', 'PUT', data=body_solicitacao)
            
            print(data_arquivo)
            print(100*"==")
            return redirect(request.path)

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'timelines':data_cent_sol_timeline,
        'tp_timelines':data_cent_sol_tp_timeline,
        'solicitacao':data_cent_sol,
        
    } 
    return render (request, 'central/central_qualidade_solicitacao.html', context)

def central_qualidadeV2(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
    #================== ARQUIVOS JSONS ==========================#
    data_cent_sol = apiResponse(request,central_solicitacao, 'GET' )
    data_cent_sol_status = apiResponse(request,central_solicitacao_status, 'GET' )
    data_setor = apiResponse(request,setor, 'GET' )
    data_tp_doc = apiResponse(request,tp_documento, 'GET' )
    data_usuarios = apiResponse(request,usuarios, 'GET' )
    
    #================== ARQUIVOS JSONS ==========================#
    
    #================== TROCA ID'S POR NOME =====================#
    for solicitacoes in data_cent_sol:
        for status in data_cent_sol_status:
            if solicitacoes['status'] == status['id']:
                solicitacoes['status'] = status['status']
        for tp_doc in data_tp_doc:
            if solicitacoes['tipo_documento'] == tp_doc['id']:
                solicitacoes['tipo_documento'] = tp_doc['nome']
        for usuarios2 in data_usuarios:
            if solicitacoes['atendente'] == usuarios2['id']:
                solicitacoes['atendente'] = usuarios2['nome']
            if solicitacoes['solicitante'] == usuarios2['id']:
                solicitacoes['solicitante'] = usuarios2['nome']
    #============================================================#
    
    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'SOL_PAD':
            nome_documento = request.POST.get('nm_doc')
            descricao_ajustes = request.POST.get('desc_doc')
            setor_esc = request.POST.get('setor')
            tipo_documento = request.POST.get('tp_doc')
            documento = request.FILES.get('documento')
            
            
            body_sol_doc = {
                "nm_doc": nome_documento,
                "comentario": descricao_ajustes,
                "tipo_documento": tipo_documento,
                "setor": setor_esc,
                "solicitante": request.session.get('id_usuario')
            }
            if documento is not None:
                files = {"arquivo": documento}
            
            data_arquivo = apiResponse(request, central_solicitacao, 'POST', data=body_sol_doc,file=files)
            
            body_timeline = {
                "comentario": "Abertura de Solicitação",
                "solicitacao": data_arquivo['id'],
                "usuario": request.session.get('id_usuario'),
                "tipo": 1
            }
            data_arquivo = apiResponse(request, central_solicitacao_timeline, 'POST', data=body_timeline)
            
            pprint.pprint(body_sol_doc)
            pprint.pprint(data_arquivo)
            return redirect(request.path)
        if '_method' in request.POST and request.POST['_method'] == 'ATEND_SOL':
            id_solicitacao = request.POST.get('id_sol')
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")  # Formatação de exemplo, ajuste conforme necessário
            body_sol_doc = {
                "atendente": request.session.get('id_usuario'),
                "status": 2,
                "data_atendimento":formatted_datetime
            }
            data_arquivo = apiResponse(request, f'{central_solicitacao}{id_solicitacao}/', 'PUT', data=body_sol_doc)

            body_timeline = {
                "comentario": "Arquivo recebido com sucesso",
                "solicitacao": id_solicitacao,
                "usuario": request.session.get('id_usuario'),
                "tipo": 2
            }
            data_arquivoPt2 = apiResponse(request, central_solicitacao_timeline, 'POST', data=body_timeline)
            
            body_timelinePt2 = {
                "comentario": "Verificando e fazendo as mudanças necessárias e solicitadas",
                "solicitacao": id_solicitacao,
                "usuario": request.session.get('id_usuario'),
                "tipo": 3
            }
            data_arquivoPt3 = apiResponse(request, central_solicitacao_timeline, 'POST', data=body_timelinePt2)
            return redirect(request.path)
        
            

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'solicitacoes':data_cent_sol,
        'setores':data_setor,
        'tp_docs':data_tp_doc,
    } 
    return render (request, 'central/central_qualidadeV2.html', context)

def central_qualidade_solicitacaoV2(request,id_solicitacao):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
   
    #================== ARQUIVOS JSONS ==========================#
    data_cent_sol = apiResponse(request,f'{central_solicitacao}{id_solicitacao}/', 'GET' )
    data_cent_sol_tp_timeline = apiResponse(request,central_solicitacao_tipo_timeline, 'GET' )
    data_cent_sol_timeline = apiResponse(request,f'{central_solicitacao_timeline}?solicitacao={id_solicitacao}', 'GET' )
    data_usuarios = apiResponse(request,usuarios, 'GET' )
    data_setor = apiResponse(request,setor, 'GET' )
    data_tp_doc = apiResponse(request,tp_documento, 'GET' )
    data_pasta = apiResponse(request,pastas, 'GET' )

    #================== ARQUIVOS JSONS ==========================#
    pprint.pprint(data_cent_sol)
    for timeline in data_cent_sol_timeline:
        #============================== AJUSTE DE DATA ==================================#
        data_objeto = datetime.strptime(timeline['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # Formatar a data para "07/01/2024" e a hora para "11:36"
        timeline['created_at'] = data_objeto.strftime("%d/%m/%Y às %H:%M")
        #================================================================================#

        #============================== TROCA DE ID'S ===================================#        
        for tp_timeline in data_cent_sol_tp_timeline:
            if timeline['tipo'] == tp_timeline['id']:
                timeline['icone'] = tp_timeline['icone']
                timeline['tp_requisicao'] = tp_timeline['descricao']
        for usuario in data_usuarios:
            if timeline['usuario'] == usuario['id']:
                timeline['usuario'] = usuario['nome']
        # URL que você deseja renderizar dentro do seu template
    
    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'INCLUSAO':
            descricao = request.POST.get('descricao')
            documento = request.FILES.get('documento')
            body_timeline = {
                "comentario": descricao,
                "solicitacao": id_solicitacao,
                "usuario": request.session.get('id_usuario'),
                "tipo": 9
            }
            if documento is not None:
                files = {"arquivo": documento}
            data_arquivo = apiResponse(request, central_solicitacao_timeline, 'POST', data=body_timeline,file=files)
            print(data_arquivo)
            return redirect(request.path)
        
        if '_method' in request.POST and request.POST['_method'] == 'SOL_VAL':
            descricao = request.POST.get('descricao')
            documento = request.FILES.get('documento')
            body_timeline = {
                "comentario": descricao,
                "solicitacao": id_solicitacao,
                "usuario": request.session.get('id_usuario'),
                "tipo": 4
            }
            body_solicitacao= {
                "status": 3
            }
            if documento is not None:
                files = {"arquivo": documento}
            data_arquivo = apiResponse(request, central_solicitacao_timeline, 'POST', data=body_timeline,file=files)
            data_arquivo2 = apiResponse(request, f'{central_solicitacao}{id_solicitacao}/', 'PUT', data=body_solicitacao)
            print(data_arquivo)
            return redirect(request.path)
        
        if '_method' in request.POST and request.POST['_method'] == 'SOL_APROV':
            descricao = request.POST.get('descricao')
            documento = request.FILES.get('documento')
            
            body_timeline = {
                "comentario": descricao,
                "solicitacao": id_solicitacao,
                "usuario": request.session.get('id_usuario'),
                "tipo": 5
            }
            body_solicitacao= {
                "status": 4
            }
            if documento is not None:
                files = {"arquivo": documento}
            data_arquivo = apiResponse(request, central_solicitacao_timeline, 'POST', data=body_timeline,file=files)
            data_arquivo2 = apiResponse(request, f'{central_solicitacao}{id_solicitacao}/', 'PUT', data=body_solicitacao)
            print(data_arquivo)
            print(data_arquivo2)
            print(100*"==")
            print(f'{data_cent_sol}{id_solicitacao}/')
            return redirect(request.path)
        
        if '_method' in request.POST and request.POST['_method'] == 'FINALIZAR':
            #=============================== PROCESSO DE FINALIZAÇÃO DA TIMELINE =======================================#
            descricao = "Finalizado processo de solicitação de padronização"
            id_pasta = request.POST.get('id_pasta')
            descricao_pasta = request.POST.get('descricao_pasta')
            data_criacao = request.POST.get('data_criacao')
            id_setor = request.POST.get('setor')
            tipo_documento = request.POST.get('tipo_documento')
            documento = request.FILES.get('arquivos')
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")  # Formatação de exemplo, ajuste conforme necessário
            body_timeline = {
                "comentario": descricao,
                "solicitacao": id_solicitacao,
                "usuario": request.session.get('id_usuario'),
                "tipo": 8
            }
            body_solicitacao= {
                "status": 5,
                "data_atendimento_encerramento":formatted_datetime
            }
            data_arquivo = apiResponse(request, central_solicitacao_timeline, 'POST', data=body_timeline)
            data_arquivo2 = apiResponse(request, f'{central_solicitacao}{id_solicitacao}/', 'PUT', data=body_solicitacao)
            #===========================================================================================================#
            #========================== PEGANDO AS SIGLAS ==========================#
            data_arquivo = apiResponse(request,f'{arquivos}?pasta={id_pasta}', 'GET' )
            data_set_sig = apiResponse(request,f'{setor_sigla}?setor={id_setor}', 'GET' )
            nm_set = data_set_sig[0]['sigla']
            
            data_tp_doc = apiResponse(request,f'{tp_documento}{tipo_documento}/', 'GET' )
            nm_tp_doc = data_tp_doc['sigla']
            nm_tp_doc = nm_tp_doc.upper()
            validade_tp_doc = data_tp_doc['validade']
            print(100*'=')
            # Convertendo a string para um objeto datetime
            data_inicial = datetime.strptime(data_criacao, '%Y-%m-%d')

            # Adicionando a quantidade de anos desejada, considerando anos bissextos
            nova_data = data_inicial + relativedelta(years=validade_tp_doc)

            # Convertendo o resultado de volta para uma string
            nova_data_str = nova_data.strftime('%Y-%m-%d')

            # Exibindo a nova data como string
            print(nova_data_str)
            print(100*'=')
            data_arquivo = apiResponse(request,f'{arquivos}?pasta={id_pasta}', 'GET' )
            # Obter a quantidade total de itens
            quantidade_total = len(data_arquivo)
            quantidade_total += 1
            quantidade_formatada = str(quantidade_total).zfill(3)
            #=======================================================================#
            body_doc = {
                "codigo": f'{nm_tp_doc}.{nm_set}{quantidade_formatada}',
                "descricao": f'{descricao_pasta}',
                "data_emissao": f'{data_criacao}',
                "prox_revisao": f'{nova_data_str}',
                "pasta": f'{id_pasta}',
                "setor": f'{id_setor}',
                "tipo_documento": f'{tipo_documento}',
                "responsavel": request.session.get('id_usuario')
            }
            if documento is not None:
                files = {"arquivo": documento}
            dataresposta = apiResponse(request, arquivos, 'POST', data=body_doc, file=files)
            print(dataresposta)            

            return redirect(request.path)
        
        if '_method' in request.POST and request.POST['_method'] == 'VALIDAR':
            descricao = request.POST.get('descricao')
            body_timeline = {
                "comentario": descricao,
                "solicitacao": id_solicitacao,
                "usuario": request.session.get('id_usuario'),
                "tipo": 7
            }
            body_solicitacao= {
                "status": 2
            }
            data_arquivo = apiResponse(request, central_solicitacao_timeline, 'POST', data=body_timeline)
            data_arquivo2 = apiResponse(request, f'{central_solicitacao}{id_solicitacao}/', 'PUT', data=body_solicitacao)
            
            print(data_arquivo)
            print(100*"==")
            return redirect(request.path)
        
        if '_method' in request.POST and request.POST['_method'] == 'N_VALIDAR':
            descricao = request.POST.get('descricao')
            body_timeline = {
                "comentario": descricao,
                "solicitacao": id_solicitacao,
                "usuario": request.session.get('id_usuario'),
                "tipo": 10
            }
            body_solicitacao= {
                "status": 2
            }
            data_arquivo = apiResponse(request, central_solicitacao_timeline, 'POST', data=body_timeline)
            data_arquivo2 = apiResponse(request, f'{central_solicitacao}{id_solicitacao}/', 'PUT', data=body_solicitacao)
            
            print(data_arquivo)
            print(100*"==")
            return redirect(request.path)
    
            
            
        
            
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'timelines':data_cent_sol_timeline,
        'tp_timelines':data_cent_sol_tp_timeline,
        'solicitacao':data_cent_sol,
        'setores':data_setor,
        'tp_docs':data_tp_doc,
        'pastas':data_pasta
    } 
    return render (request, 'central/central_qualidade_solicitacaoV2.html', context)
