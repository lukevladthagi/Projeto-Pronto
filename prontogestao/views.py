from django.shortcuts import render
from administrativo.views import apiResponse, host, verifica_headers
from django.shortcuts import render, redirect
import requests, json, pprint, pytz, datetime
from django.http import JsonResponse
import calendar , locale
from collections import defaultdict

url_usuarios = 'http://192.168.4.33:8000/users/'
urlInd = 'http://192.168.4.33:8000/prontogestao/indicadores/'
urlResult = 'http://192.168.4.33:8000/prontogestao/resultado/'
urlItem = "http://192.168.4.33:8000/prontogestao/itemindicador/"
urlCargos = "http://192.168.4.33:8000/cargos/"
urlEscolaridade = "http://192.168.4.33:8000/escolaridade/"
urlMetas = f"http://192.168.4.33:8000/prontogestao/metaGesProd/"
urlMetaProj = f"http://192.168.4.33:8000/prontogestao/metaProj/"
urlMetaReal = f"http://192.168.4.33:8000/prontogestao/metaReal/"
urlGestores = "http://192.168.4.33:8000/usuarios/?funcao=1,2,3,4,5"

def cadastroGestao(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    return render (request, 'cadastro-gestao.html', context) 

def fichaIdentidade(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result

    data_user = apiResponse(request, url_usuarios, 'GET')
  
    if request.method == 'POST':
        print("Ok, foi post")

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'dataUser': data_user,
    }


    return render (request, 'ficha-identidade-result.html', context)

def resultPesquisa(request):

    global soma
    global valoresResp
    global tri_1

    global tri_1_0
    global tri_1_1
    global tri_1_2
    global tri_1_3

    global tri_2_0
    global tri_2_1
    global tri_2_2
    global tri_2_3

    global tri_3_0
    global tri_3_1
    global tri_3_2
    global tri_3_3

    global tri_4_0
    global tri_4_1
    global tri_4_2
    global tri_4_3

    global soma_av_1
    global soma_av_2
    global soma_av_3
    global soma_av_4

    global soma_av_1_comp
    global soma_av_2_comp
    global soma_av_3_comp
    global soma_av_4_comp

    global soma_indicadores
    global soma_indicador

    global max_total_av_desemp
    global max_total_av_comp
            

    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result

    #Consumo da api=========
    urldesG = "http://192.168.4.33:9090/prontogestao/dgeral/" 
    urlItem = "http://192.168.4.33:8000/prontogestao/itemindicador/"

    #Indicadores
    dataInd = apiResponse(request, urlInd, 'GET')
    
    #Resultado(Respostas)
    dataResult = apiResponse(request, urlResult, 'GET') 
   
    #Usuarios
    data_user = apiResponse(request, url_usuarios, 'GET')

    
    
    print(valoresResp)

    #Parte mais importante do código, o dicionário salva todas as informações com chave de indentificação e uma tupla com os valores
    soma_indicadores = {}

    #Contador de indicadores 
    cnt_indicadores = 0
    cnt_itens = 0
    cnt_itens_comp = 0

    #Soma das avaliações
    soma_av_1 = 0
    soma_av_2 = 0
    soma_av_3 = 0
    soma_av_4 = 0

    soma_av_1_comp = 0
    soma_av_2_comp = 0
    soma_av_3_comp = 0
    soma_av_4_comp = 0

    soma_ind = 0 

    soma_valores_s = 0 

    #Percorre o array de indicadores 
    for indicador in dataInd:
       
        #Se o indicador for igual a 1 (ava_desemp) 
        if indicador['tp_aval'] == 1:

            #Variável que aramazena o nome do indicador para usar como chave mais na frente 
            indicadores = indicador['titulo']

            #Incrementa contador (Realizar a média mais na frente)
            cnt_indicadores += 1
            
            #Zera as somas para não serem duplicadas mais na frente 
            soma_valores = 0
            soma_valores2 = 0
            soma_valores3 = 0
            soma_valores4 = 0
           
            #Percorre o array de resultados 
            for resultado in dataResult:
                 
                #Se o trimestre for igual a 1: 
                if resultado['trimestre'] == 1:
                    
                    #O indicador da api de resultados precisa ser o mesmo da api de indicadores 
                    if resultado['indicador'] == indicador['id']:

                        #Faz a soma da resposta de todos os itens de um indicador 
                        soma_valores += resultado['resposta']

                        #Incrementa o contador 
                        cnt_itens += 1

                        #Armazena tudo em um dicionário, nessa ordem: "[Indicador, trimestre, colaborador] = [soma] "
                        soma_indicadores[indicadores, 1, resultado['colaborador'], resultado['tp_aval']] = [soma_valores]


                #Repete para todos os outros trimestres
                #...
                if resultado['trimestre'] == 2:
                    
                    if resultado['indicador'] == indicador['id']:
                        
                        soma_valores2 += resultado['resposta']

                        soma_indicadores[indicadores, 2, resultado['colaborador'], resultado['tp_aval']] = [soma_valores2]


                if resultado['trimestre'] == 3:
                    
                    if resultado['indicador'] == indicador['id']:
                        
                        soma_valores3 += resultado['resposta']
                        
                        soma_indicadores[indicadores, 3, resultado['colaborador'], resultado['tp_aval']] = [soma_valores3]
                        
                    
                if resultado['trimestre'] == 4:
                    
                    if resultado['indicador'] == indicador['id']:
                        
                        soma_valores4 += resultado['resposta']

                        soma_indicadores[indicadores, 4, resultado['colaborador'], resultado['tp_aval']] = [soma_valores4] 

                max_total_av_desemp = cnt_itens * 4

        
        if indicador['tp_aval'] == 2:

            #Variável que aramazena o nome do indicador para usar como chave mais na frente 
            indicadores = indicador['titulo']

            #Incrementa contador (Realizar a média mais na frente)
            cnt_indicadores += 1
            
            #Zera as somas para não serem duplicadas mais na frente 
            soma_valores = 0
            soma_valores2 = 0
            soma_valores3 = 0
            soma_valores4 = 0
            
        
            #Percorre o array de resultados 
            for resultado in dataResult:
                
                #Se o trimestre for igual a 1: 
                if resultado['trimestre'] == 1:
                    
                    #O indicador da api de resultados precisa ser o mesmo da api de indicadores 
                    if resultado['indicador'] == indicador['id']:

                        #Faz a soma da resposta de todos os itens de um indicador 
                        soma_valores += resultado['resposta']

                        #Incrementa o contador 
                        cnt_itens_comp += 1

                        #Armazena tudo em um dicionário, nessa ordem: "[Indicador, trimestre, colaborador] = [soma] "
                        soma_indicadores[indicadores, 1, resultado['colaborador'], 2] = [soma_valores]


                #Repete para todos os outros trimestres
                #...
                if resultado['trimestre'] == 2:
                    
                    if resultado['indicador'] == indicador['id']:
                        
                        soma_valores2 += resultado['resposta']

                        soma_indicadores[indicadores, 2, resultado['colaborador'], 2] = [soma_valores2]


                if resultado['trimestre'] == 3:
                    
                    if resultado['indicador'] == indicador['id']:
                        
                        soma_valores3 += resultado['resposta']
                        
                        soma_indicadores[indicadores, 3, resultado['colaborador'], 2] = [soma_valores3]
                        
                    
                if resultado['trimestre'] == 4:
                    
                    if resultado['indicador'] == indicador['id']:
                        
                        soma_valores4 += resultado['resposta']

                        soma_indicadores[indicadores, 4, resultado['colaborador'], 2] = [soma_valores4] 
                
                max_total_av_comp = cnt_itens_comp * 4
            

    

    #Variavel que armazena o maximo total de uma avaliação
    

    #Percorre o dicionário
    for indicadores, soma_valores in soma_indicadores.items():
        
        if indicadores[3] == 1:

            #Verifica se o trimestre de referência é o 1 
            if indicadores[1] == 1:

                #Soma e armazena tudo que for referente ao trimestre 1 
                soma_av_1 += soma_valores[0]
                
            #Repete para os outros trimestres 
            #...

            if indicadores[1] == 2:
                soma_av_2 += soma_valores[0]
                
            if indicadores[1] == 3:
                soma_av_3 += soma_valores[0]
                
            if indicadores[1] == 4:
                soma_av_4 += soma_valores[0]

    
    for indicadores, soma_valores in soma_indicadores.items():
        
        if indicadores[3] == 2:
            print("entrou no loop")

            #Verifica se o trimestre de referência é o 1 
            if indicadores[1] == 1:

                #Soma e armazena tudo que for referente ao trimestre 1 
                soma_av_1_comp += soma_valores[0]
                print(f'soma valores av 1 {soma_av_1_comp}')
            #Repete para os outros trimestres 
            #...

            if indicadores[1] == 2:
                soma_av_2_comp += soma_valores[0]
                
            if indicadores[1] == 3:
                soma_av_3_comp += soma_valores[0]
                
            if indicadores[1] == 4:
                soma_av_4_comp += soma_valores[0]


    resultado = None
    soma_indicador = {} 

    tri_cnt1 = 0
    tri_cnt2 = 0
    tri_cnt3 = 0
    tri_cnt4 = 0

    tri_1 = {}
    tri_2 = {}
    tri_3 = {}
    tri_4 = {}
    
    # Percorre a api de indicadores 
    for indicador in dataInd:

        #Verifica se a avaliação é do tipo desempenho 
        if indicador['tp_aval'] == 1:

            #Percorre o dicionario principal 
            for indicadores, soma_valores in soma_indicadores.items():

                #Se o indicador na posição 0 (Referente ao nome do indicador) for igual ao indicador da api e trimestre de ref 1 =
                if indicadores[0] == indicador['titulo'] and indicadores[1] == 1:
                    tri_cnt1 += 1
                    tri_1[indicador['titulo']] = soma_valores[0]
                    

                #Repete para os outros trimestres 
                #...
                if indicadores[0] == indicador['titulo'] and indicadores[1] == 2:
                    tri_cnt2 += 1
                    tri_2[indicador['titulo']] = soma_valores[0]  
                    
               
                if indicadores[0] == indicador['titulo'] and indicadores[1] == 3:
                    tri_cnt3 += 1
                    tri_3[indicador['titulo']] = soma_valores[0]  
                    
          
                if indicadores[0] == indicador['titulo'] and indicadores[1] == 4:
                    tri_cnt4 += 1
                    tri_4[indicador['titulo']] = soma_valores[0]  
                    
                  
                
    # Variaveis para o gráfico 

    # Para passar as variaveis do python para o gráfico em Java Script, eu passo cada valor referente ao trimestre de modo automático
    # tri_1_0 é a mesma coisa que Trimestre 1 na posição 0, pois, no gráfico, as informações são dispostas uma após a outra, 4 vezes.
    # Temos 4 posições para cada um dos 4 trimestres.

    print("=================================")

    # Trimestre 1 posição 0:
    # Busca no dicionario a chave "Assiduidade", referente ao primeiro trimestre
    # Pega o valor da chave e armazena na variavel

    tri_1_0 = tri_1.get("Assiduidade")
    

    #Trimestre 1 posição 1:
    tri_1_1 = tri_1.get("Motivação")
   

    #Trimestre 1 posição 2:
    tri_1_2 = tri_1.get("Disciplina")
   

    #Trimestre 1 posição 3:
    tri_1_3 = tri_1.get("Responsabilidade")
    

    # Repete para os outros trimestres
    #...
    tri_2_0 = tri_2.get("Assiduidade")
    
    tri_2_1 = tri_2.get("Motivação")
   
    tri_2_2 = tri_2.get("Disciplina")
    
    tri_2_3 = tri_2.get("Responsabilidade")
   

    tri_3_0 = tri_3.get("Assiduidade")
  
    tri_3_1 = tri_3.get("Motivação")
    
    tri_3_2 = tri_3.get("Disciplina")

    tri_3_3 = tri_3.get("Responsabilidade")
   

    tri_4_0 = tri_4.get("Assiduidade")
    
    tri_4_1 = tri_4.get("Motivação")
   
    tri_4_2 = tri_4.get("Disciplina")
   
    tri_4_3 = tri_4.get("Responsabilidade")

    

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'dataUser': data_user,
    }

    return render (request, 'resultpesquisa.html', context)

def avaDesempgeral(request):

    global indicador
    global valoresResp
    global tri_1

    global tri_1_0
    global tri_1_1
    global tri_1_2
    global tri_1_3

    global tri_2_0
    global tri_2_1
    global tri_2_2
    global tri_2_3

    global tri_3_0
    global tri_3_1
    global tri_3_2
    global tri_3_3

    global tri_4_0
    global tri_4_1
    global tri_4_2
    global tri_4_3
    global opcao_value1

    #Funções padrões 
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result

    #Consumo da api=========
    urldesG = "http://192.168.4.33:9090/prontogestao/dgeral/" 

    #Indicadores
    dataInd = apiResponse(request, urlInd, 'GET')
    #Itens(Perguntas)
    dataItem = apiResponse(request, urlItem, 'GET')
    #Resultado(Respostas)
    dataResult = apiResponse(request, urlResult, 'GET') 
    #Usuarios
    data_user = apiResponse(request, url_usuarios, 'GET')
    

    var_value_tri_1 = 0
    var_value_tri_2 = 0
    var_value_tri_3 = 0
    var_value_tri_4 = 0

    opcao_value1 = {}

    # Se o método do HTML for POST 
    if request.method == 'POST': 
        
        # Percorre o json de indicadores 
        for ind in dataInd:
            # Se o tipo de avaliação for igual a 1 ( Avaliação de desempenho geral )
            if ind['tp_aval'] == 1:

                # Pega o indicador 
                indicador = request.POST.get('indicador_id' + str(ind['id']))

                # Percorre o json de itens 
                for item in dataItem:

                    # Se o id do indicador for o mesmo do item, então:
                    if ind['id'] == item['indicador']:

                        # Pega a pergunta 
                        item_perg = request.POST.get('item_id' + str(item['id']))
                        
                        # Pega o trimestre 1 
                        str_tri_1 = request.POST.get('res_tri_1' + str(item['id']))
                        
                        # Se ele nao for None 
                        if str_tri_1 is not NoneType:
                            
                            # Separa a string (Ex:. 1.1 ---> Valor = 1 , Trimestre = 1)
                            split_tri1 = str_tri_1.split(".")

                            # Tratativa de erro para caso o usuário não selecione um valor válido
                            if len(split_tri1) >= 2:

                                # Pega a posição [0] da string (Referente a valor)
                                var_value_tri_1 = split_tri1[0]

                                opcao_value1[item['indicador']] = var_value_tri_1
                                
                                
                                # Pega a posição [1] da string (Referente a trimestre )
                                tri_1 = split_tri1[1]

                                # Salvar dados 
                                data_resp = {
                                "resposta": str(var_value_tri_1),
                                "colaborador": 1,
                                "tp_aval": 1,
                                "indicador": int(indicador),
                                "it_indic": int(item_perg),
                                "trimestre": int(tri_1), 
                                }

                                # Faz um post na api 
                                data_resultado  = apiResponse(request, urlResult, 'POST', data=data_resp)
                                print("=============Resultado 1===============")
                                pprint.pprint(data_resultado)
                            
                            else:
                                pass
                        
                        # ==== Repete os mesmos passos para 2º, 3º e 4º trimestre ====

                        str_tri_2 = request.POST.get('res_tri_2' + str(item['id']))
                        if str_tri_2 is not None:
                            split_tri2 = str_tri_2.split(".")
                            if len(split_tri2) >= 2:
                                var_value_tri_2 = split_tri2[0]
                                tri_2 = split_tri2[1]

                                data_resp = {
                                "resposta": str(var_value_tri_2),
                                "colaborador": 1,
                                "tp_aval": 1,
                                "indicador": int(indicador),
                                "it_indic": int(item_perg),
                                "trimestre": int(tri_2), 
                                }
                                
                                data20 = apiResponse(request, urlResult, 'POST', data=data_resp)
                                print("=============Resultado 2===============")
                                pprint.pprint(data20)

                            else:
                                pass
                        
                        str_tri_3 = request.POST.get('res_tri_3' + str(item['id']))
                        if str_tri_3 is not None:
                            split_tri3 = str_tri_3.split(".")
                            if len(split_tri3) >= 2:
                                var_value_tri_3 = split_tri3[0]
                                tri_3 = split_tri3[1]


                                data_resp = {
                                "resposta": str(var_value_tri_3),
                                "colaborador": 1,
                                "tp_aval": 1,
                                "indicador": int(indicador),
                                "it_indic": int(item_perg),
                                "trimestre": int(tri_3), 
                                }

                                data20 = apiResponse(request, urlResult, 'POST', data=data_resp)
                                print("=============Resultado 3===============")
                                pprint.pprint(data20)

                            else:
                                pass
                        
                        
                        str_tri_4 = request.POST.get('res_tri_4' + str(item['id']))
                        if str_tri_4 is not None:
                            split_tri4 = str_tri_4.split(".")
                            if len(split_tri4) >= 2:
                                var_value_tri_4 = split_tri4[0]
                                tri_4 = split_tri4[1]

                                data_resp = {
                                "resposta": str(var_value_tri_4),
                                "colaborador": 1,
                                "tp_aval": 1,
                                "indicador": int(indicador),
                                "it_indic": int(item_perg),
                                "trimestre": int(tri_4), 
                                }

                                data20  = apiResponse(request, urlResult, 'POST', data=data_resp)
                                print("=============Resultado 4===============")
                                pprint.pprint(data20)
                       
                            else:
                                pass
        

        return redirect('/prontocardio/prontogestao/ava_finalizada/')  


        
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'indicadores': dataInd,
        'itemindicador': dataItem,
        'dataResult': dataResult,
        'tri_1': tri_1,

        'tri_1_0': tri_1_0,
        'tri_1_1': tri_1_1,
        'tri_1_2': tri_1_2,
        'tri_1_3': tri_1_3,
        'tri_2_0': tri_2_0,
        'tri_2_1': tri_2_1,
        'tri_2_2': tri_2_2,
        'tri_2_3': tri_2_3,
        'tri_3_0': tri_3_0,
        'tri_3_1': tri_3_1,
        'tri_3_2': tri_3_2,
        'tri_3_3': tri_3_3,
        'tri_4_0': tri_4_0,
        'tri_4_1': tri_4_1,
        'tri_4_2': tri_4_2,
        'tri_4_3': tri_4_3,
        'var_value_tri_1': str(var_value_tri_1),
        'opcao_value': opcao_value1,
        
    }

    return render (request, 'ava-desemp-geral.html', context) 

def avaliacaoCompetencia(request):
    global indicador
    global valoresResp
    global tri_1

    global tri_1_0
    global tri_1_1
    global tri_1_2
    global tri_1_3

    global tri_2_0
    global tri_2_1
    global tri_2_2
    global tri_2_3

    global tri_3_0
    global tri_3_1
    global tri_3_2
    global tri_3_3

    global tri_4_0
    global tri_4_1
    global tri_4_2
    global tri_4_3
    global opcao_value1

    #Funções padrões 
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result

    #Consumo da api=========
    urldesG = "http://192.168.4.33:9090/prontogestao/dgeral/" 

    #Indicadores
    dataInd = apiResponse(request, urlInd, 'GET')
    #Itens(Perguntas)
    dataItem = apiResponse(request, urlItem, 'GET')
    #Resultado(Respostas)
    dataResult = apiResponse(request, urlResult, 'GET') 
    #Usuarios
    data_user = apiResponse(request, url_usuarios, 'GET')
    

    var_value_tri_1 = 0
    var_value_tri_2 = 0
    var_value_tri_3 = 0
    var_value_tri_4 = 0

    opcao_value1 = {}

    # Se o método do HTML for POST 
    if request.method == 'POST': 
        
        # Percorre o json de indicadores 
        for ind in dataInd:
            # Se o tipo de avaliação for igual a 1 ( Avaliação de desempenho geral )
            if ind['tp_aval'] == 2:

                # Pega o indicador 
                indicador = request.POST.get('indicador_id' + str(ind['id']))

                # Percorre o json de itens 
                for item in dataItem:

                    # Se o id do indicador for o mesmo do item, então:
                    if ind['id'] == item['indicador']:

                        # Pega a pergunta 
                        item_perg = request.POST.get('item_id' + str(item['id']))
                        
                        # Pega o trimestre 1 
                        str_tri_1 = request.POST.get('res_tri_1' + str(item['id']))
                        
                        # Se ele nao for None 
                        if str_tri_1 is not NoneType:
                            
                            # Separa a string (Ex:. 1.1 ---> Valor = 1 , Trimestre = 1)
                            split_tri1 = str_tri_1.split(".")

                            # Tratativa de erro para caso o usuário não selecione um valor válido
                            if len(split_tri1) >= 2:

                                # Pega a posição [0] da string (Referente a valor)
                                var_value_tri_1 = split_tri1[0]

                                opcao_value1[item['indicador']] = var_value_tri_1
                                
                                
                                # Pega a posição [1] da string (Referente a trimestre )
                                tri_1 = split_tri1[1]

                                # Salvar dados 
                                data_resp = {
                                "resposta": str(var_value_tri_1),
                                "colaborador": 1,
                                "tp_aval": 2,
                                "indicador": int(indicador),
                                "it_indic": int(item_perg),
                                "trimestre": int(tri_1), 
                                }

                                # Faz um post na api 
                                data_resultado  = apiResponse(request, urlResult, 'POST', data=data_resp)
                                print("=============Resultado 1===============")
                                pprint.pprint(data_resultado)
                            
                            else:
                                pass
                        
                        # ==== Repete os mesmos passos para 2º, 3º e 4º trimestre ====

                        str_tri_2 = request.POST.get('res_tri_2' + str(item['id']))
                        if str_tri_2 is not None:
                            split_tri2 = str_tri_2.split(".")
                            if len(split_tri2) >= 2:
                                var_value_tri_2 = split_tri2[0]
                                tri_2 = split_tri2[1]

                                data_resp = {
                                "resposta": str(var_value_tri_2),
                                "colaborador": 1,
                                "tp_aval": 2,
                                "indicador": int(indicador),
                                "it_indic": int(item_perg),
                                "trimestre": int(tri_2), 
                                }

                                data20  = apiResponse(request, urlResult, 'POST', data=data_resp)
                                print("=============Resultado 2===============")
                                pprint.pprint(data20)

                            else:
                                pass
                        
                        str_tri_3 = request.POST.get('res_tri_3' + str(item['id']))
                        if str_tri_3 is not None:
                            split_tri3 = str_tri_3.split(".")
                            if len(split_tri3) >= 2:
                                var_value_tri_3 = split_tri3[0]
                                tri_3 = split_tri3[1]


                                data_resp = {
                                "resposta": str(var_value_tri_3),
                                "colaborador": 1,
                                "tp_aval": 2,
                                "indicador": int(indicador),
                                "it_indic": int(item_perg),
                                "trimestre": int(tri_3), 
                                }

                                responseresult = requests.post(url=urlResult, data=data_resp, headers=headers)
                                data20  = responseresult.json()
                                print("=============Resultado 3===============")
                                pprint.pprint(data20)

                            else:
                                pass
                        
                        
                        str_tri_4 = request.POST.get('res_tri_4' + str(item['id']))
                        if str_tri_4 is not None:
                            split_tri4 = str_tri_4.split(".")
                            if len(split_tri4) >= 2:
                                var_value_tri_4 = split_tri4[0]
                                tri_4 = split_tri4[1]

                                data_resp = {
                                "resposta": str(var_value_tri_4),
                                "colaborador": 1,
                                "tp_aval": 2,
                                "indicador": int(indicador),
                                "it_indic": int(item_perg),
                                "trimestre": int(tri_4), 
                                }

                                
                                responseresult = requests.post(url=urlResult, data=data_resp, headers=headers)
                                data20  = responseresult.json()
                                print("=============Resultado 4===============")
                                pprint.pprint(data20)
                       
                            else:
                                pass
        

        return redirect('/prontocardio/prontogestao/ava_finalizada/')  

        
        
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'indicadores': dataInd,
        'itemindicador': dataItem,
        'dataResult': dataResult,
        'tri_1': tri_1,

        'tri_1_0': tri_1_0,
        'tri_1_1': tri_1_1,
        'tri_1_2': tri_1_2,
        'tri_1_3': tri_1_3,
        'tri_2_0': tri_2_0,
        'tri_2_1': tri_2_1,
        'tri_2_2': tri_2_2,
        'tri_2_3': tri_2_3,
        'tri_3_0': tri_3_0,
        'tri_3_1': tri_3_1,
        'tri_3_2': tri_3_2,
        'tri_3_3': tri_3_3,
        'tri_4_0': tri_4_0,
        'tri_4_1': tri_4_1,
        'tri_4_2': tri_4_2,
        'tri_4_3': tri_4_3,
        'var_value_tri_1': str(var_value_tri_1),
        'opcao_value': opcao_value1,
        
    }


    return render (request, 'avaliacao-competencia.html', context) 

def autoAvacomp(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result


    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    return render (request, 'auto-ava-comp.html', context) 

def ava_finalizada(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result


    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    return render(request, 'ava-finalizada.html', context)

def selecionar_trimestre(request):

    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result

    
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
    }

    if request.method == 'POST':
        select_tri = request.POST.get('select_tri')
        print(select_tri)

        if int(select_tri) == 1:
           print("ok, funciona")
        

    return render(request, 'selecionar-trimestre.html', context)

def relatorio_gestao(request,id_usuario, id_aval, id_trimestre):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
    #Indicadores
    dataInd = apiResponse(request, f"http://{host}/prontogestao/indicadores/?tp_aval={id_aval}", 'GET')
    #Itens(Perguntas)
    dataItem = apiResponse(request, f"http://{host}/prontogestao/itemindicador/?tp_aval={id_aval}", 'GET')
    #Usuario
    dataUsuarios = apiResponse(request, f"http://{host}/usuarios/{id_usuario}/", 'GET')
    #Trimestre
    dataTrimestre = apiResponse(request, f"http://{host}/prontogestao/trimestre/{id_trimestre}/", 'GET')
    #Respostas
    dataResp = apiResponse(request, f"http://{host}/prontogestao/resultado/?colaborador={id_usuario}&tp_aval={id_aval}", 'GET')


    trimestres = defaultdict(dict)

    for item in dataResp:
        trimestre = item['trimestre']
        indicador = item['indicador']
        if trimestre not in trimestres:
            trimestres[trimestre]['colaborador'] = item['colaborador']
            trimestres[trimestre]['indicador'] = 0
            trimestres[trimestre]['resposta'] = 0
            trimestres[trimestre]['tp_aval'] = 0
            trimestres[trimestre]['it_indic'] = defaultdict(int)
        trimestres[trimestre]['indicador'] += indicador
        trimestres[trimestre]['resposta'] += item['resposta']
        trimestres[trimestre]['tp_aval'] += item['tp_aval']
        trimestres[trimestre]['it_indic'][indicador] += item['resposta']
    pprint.pprint(trimestres)
    trimestres2 = []

    # Iterando sobre os itens do dicionário
    for chave, valor in trimestres.items():
        tri_0 = valor['it_indic'].get(1, 0)
        tri_1 = valor['it_indic'].get(2, 0)
        tri_2 = valor['it_indic'].get(3, 0)
        tri_3 = valor['it_indic'].get(4, 0)
        trimestres2.append([tri_0, tri_1, tri_2, tri_3])
        
    pprint.pprint(trimestres2)

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'usuario_nome':dataUsuarios,
        'indicadores': dataInd,
        'itemindicador': dataItem,
        'respostas':dataResp,
        'trim':dataTrimestre,
        'usuario':id_usuario,
        'resultados':trimestres2
    }
    for i in range(1, 5):
        for j in range(4):
            try:
                valor = trimestres2[i-1][j]
            except IndexError:
                valor = 0
            chave = f'tri_{i}_{j}'
            context[chave] = valor

    return render(request, 'relatorio-gestao.html', context)

#=====================PESQUISA COLABORADOR================================#
def ordenar_por_nome(array):
    return sorted(array, key=lambda x: x['nome'])

def pesquisaCol(request):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
    #================================ARQUIVOS JSON===========================# 
    dataGestores = apiResponse(request,urlGestores, 'GET' )
    gestores = ordenar_por_nome(dataGestores)
    pprint.pprint(gestores)
    #========================================================================#
    
    if request.method == 'POST':
        print("Ok, foi post")
        id_colaborador = request.POST.get('id_colaborador')
        if not id_colaborador:
            return redirect(f'/prontocardio/prontogestao/lista_colaborador/geral')
        return redirect(f'/prontocardio/prontogestao/ficha_colaborador/{id_colaborador}')

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'gestores':gestores
    }
    return render(request, 'pesquisa-colaborador.html', context)

#=====================lISTAGEM COLABORADOR================================#
#===================ordem alfabedica======================================#

def consolidar_por_colaborador(nomecolaborador):
    consolidado_por_colaborador = {}
    print("ok") 
    for nomecolaborador in nomecolaborador:
        colaborador = nomecolaborador["nome"]

        if colaborador in consolidado_por_colaborador:
            consolidado_por_colaborador[colaborador].append(nomecolaborador)
        else:
            consolidado_por_colaborador[colaborador] = [nomecolaborador]

    # Organiza o dicionário por ordem alfabética das chaves (nomes dos prestadores)
    consolidado_por_colaborador_ordenado = dict(sorted(consolidado_por_colaborador.items()))

    return consolidado_por_colaborador_ordenado

#===================================================================================#


def listaColaborador(request, nome):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    if nome == 'geral':
        urlUsuarios = f"http://192.168.4.33:8000/usuarios/?funcao=1,2,3,4,5"
    else:
        urlUsuarios = f"http://192.168.4.33:8000/usuarios/?funcao=1,2,3,5,4&search={nome}"
    
    dataUsuarios = apiResponse(request, urlUsuarios, 'GET')
    dataCargos = apiResponse(request, urlCargos, 'GET')
    pprint.pprint(dataUsuarios)

    for item in dataUsuarios:
        print(item['nome'])
        dataAbertura = item['admissao']
        dataAbertura = dataAbertura[0:10]
        print('Em cima')
        print(dataAbertura)
        item['admissao'] = dataAbertura

        dataAbertura = item['admissao']
        data_objeto = datetime.datetime.fromisoformat(dataAbertura)
        data_formatada = data_objeto.strftime("%d/%m/%Y")
        item['admissao'] = data_formatada
        mes_da_resposta = item['admissao'][:10]
        item['admissao'] = mes_da_resposta

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'usuarios':dataUsuarios,
        'cargos':dataCargos
    }
    return render(request, 'listagem-colaborador.html', context)

#=====================FICHA COLABORADOR================================#
def fichaColaborador(request, id_user):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
    urlUsuarios = f"http://192.168.4.33:8000/usuarios/{id_user}/"
    urlRespostas = f"http://192.168.4.33:8000/prontogestao/resultado/?colaborador={id_user}"

    dataUsuarios = apiResponse(request, urlUsuarios, 'GET')
    dataResposta = apiResponse(request, urlRespostas, 'GET')


    urlCargos = f"http://192.168.4.33:8000/cargos/{dataUsuarios['funcao']}/"
    responseCargos = requests.get(url=urlCargos, headers=headers)
    dataCargos = apiResponse(request, urlCargos, 'GET')

    urlEscolaridade = f"http://192.168.4.33:8000/escolaridade/{dataUsuarios['escolaridade']}/"
    dataEsco = apiResponse(request, urlEscolaridade, 'GET')

    trimestres = defaultdict(dict)

    for item in dataResposta:
        trimestre = item['trimestre']
        indicador = item['indicador']
        if trimestre not in trimestres:
            trimestres[trimestre]['colaborador'] = item['colaborador']
            trimestres[trimestre]['indicador'] = 0
            trimestres[trimestre]['resposta'] = 0
            trimestres[trimestre]['tp_aval'] = 0
            trimestres[trimestre]['it_indic'] = defaultdict(int)
        trimestres[trimestre]['indicador'] += indicador
        trimestres[trimestre]['resposta'] += item['resposta']
        trimestres[trimestre]['tp_aval'] += item['tp_aval']
        trimestres[trimestre]['it_indic'][indicador] += item['resposta']
    trimestres2 = []
    #===Alterando sobre os itens do dicionário=====#
    for valor in trimestres.values():
        trimestre = list(valor['it_indic'].values())
        trimestres2.append(trimestre)
    #===============================================#    
    #============Alterar data de admissão===========#
    dataAbertura = dataUsuarios['admissao']
    dataAbertura = dataAbertura[0:10]
    dataUsuarios['admissao'] = dataAbertura

    dataAbertura = dataUsuarios['admissao']
    data_objeto = datetime.datetime.fromisoformat(dataAbertura)
    data_formatada = data_objeto.strftime("%d/%m/%Y")
    dataUsuarios['admissao'] = data_formatada
    mes_da_resposta = dataUsuarios['admissao'][:10]
    dataUsuarios['admissao'] = mes_da_resposta
    #===============================================#
        
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'usuario_nome':dataUsuarios,
        'cargo':dataCargos,
        'escolaridade':dataEsco        
    }
    return render (request, 'ficha-colaborador.html', context)

#=====================AVALIAÇÃO DE DESEMPENHO GERAL================================#
def avDesempGeral(request, id_usuario, id_aval, id_trimestre):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    #Indicadores
    dataInd = apiResponse(request, f"http://{host}/prontogestao/indicadores/?tp_aval={id_aval}", 'GET')
    #Itens(Perguntas)
    dataItem = apiResponse(request, f"http://{host}/prontogestao/itemindicador/?tp_aval={id_aval}", 'GET')
    #Usuario
    dataUsuarios = apiResponse(request, f"http://{host}/usuarios/{id_usuario}/", 'GET')
    #Trimestre
    dataTrimestre = apiResponse(request, f"http://{host}/prontogestao/trimestre/{id_trimestre}/", 'GET')
    #Respostas
    dataResp = apiResponse(request, f"http://{host}/prontogestao/resultado/?colaborador={id_usuario}&tp_aval={id_aval}", 'GET')


    trimestres = defaultdict(dict)

    for item in dataResp:
        trimestre = item['trimestre']
        indicador = item['indicador']
        if trimestre not in trimestres:
            trimestres[trimestre]['colaborador'] = item['colaborador']
            trimestres[trimestre]['indicador'] = 0
            trimestres[trimestre]['resposta'] = 0
            trimestres[trimestre]['tp_aval'] = 0
            trimestres[trimestre]['it_indic'] = defaultdict(int)
        trimestres[trimestre]['indicador'] += indicador
        trimestres[trimestre]['resposta'] += item['resposta']
        trimestres[trimestre]['tp_aval'] += item['tp_aval']
        trimestres[trimestre]['it_indic'][indicador] += item['resposta']
    pprint.pprint(trimestres)
    trimestres2 = []

    # Iterando sobre os itens do dicionário
    for chave, valor in trimestres.items():
        tri_0 = valor['it_indic'].get(1, 0)
        tri_1 = valor['it_indic'].get(2, 0)
        tri_2 = valor['it_indic'].get(3, 0)
        tri_3 = valor['it_indic'].get(4, 0)
        trimestres2.append([tri_0, tri_1, tri_2, tri_3])
        
    pprint.pprint(trimestres2)

    if request.method == 'POST':
        print(f'Avaliado:{dataUsuarios["nome"]}')
        for item in dataItem:
            for indicador in dataInd:
                if item['indicador'] == indicador['id']:
                    indic_id  = indicador["id"]
                    item_id  = item["id"]
                    data_resp = {
                        "colaborador": id_usuario,
                        "tp_aval":id_aval,
                        "indicador": indic_id,
                        "it_indic": item_id,
                    }
                    resp_tri = request.POST.get('res_tri{}'.format(item_id))

                    if resp_tri is not None:
                        data_resp["resposta"] = resp_tri
                        data_resp["trimestre"] = id_trimestre 
                        data20 = apiResponse(request, f'http://{host}/prontogestao/resultado/', 'POST', data=data_resp)
                        print(data20)
 
                    print('====================================================')
                    print(indicador['titulo'])
                    print(item['item'])
                    print(f'Trimestre é:{resp_tri}')

                    print('====================================================')
        return redirect(f'/prontocardio/prontogestao/avDesGeralFinal/{id_usuario}')

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'usuario_nome':dataUsuarios,
        'indicadores': dataInd,
        'itemindicador': dataItem,
        'respostas':dataResp,
        'trim':dataTrimestre,
        'usuario':id_usuario
    }
    for i in range(1, 5):
        for j in range(4):
            try:
                valor = trimestres2[i-1][j]
            except IndexError:
                valor = 0
            chave = f'tri_{i}_{j}'
            context[chave] = valor

    return render (request, 'avDesempGeral.html', context)

def avDesGeralFinal(request, id_usuario):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result

    urlUsuarios = f"http://192.168.4.33:8000/usuarios/{id_usuario}/"
    dataUsuarios = apiResponse(request, urlUsuarios, 'GET')

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'usuario':dataUsuarios
    }
    return render(request, 'avDesempGeralFinalizado.html', context)

#=====================AVALIAÇÃO DE COMPETENCIA===============================#
def avCompetencia(request, id_usuario, id_aval, id_trimestre):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
        
    urlUsuarios = f"http://192.168.4.33:8000/usuarios/{id_usuario}/"
    urlInd = f"http://192.168.4.33:8000/prontogestao/indicadores/?tp_aval={id_aval}"
    urlItem = f"http://192.168.4.33:8000/prontogestao/itemindicador/?tp_aval={id_aval}"
    urlResp2 = f"http://192.168.4.33:8000/prontogestao/resultado/"
    urltrim = f"http://192.168.4.33:8000/prontogestao/trimestre/{id_trimestre}/"
    #Indicadores
    dataInd = apiResponse(request, urlInd, 'GET')
    #Itens(Perguntas)
    dataItem = apiResponse(request, urlItem, 'GET')
    #Usuarios
    dataUsuarios = apiResponse(request, urlUsuarios, 'GET')
    #Trimestre
    dataTrimestre = apiResponse(request, urltrim, 'GET')

    urlResp = f"http://192.168.4.33:8000/prontogestao/resultado/?colaborador={id_usuario}&tp_aval={id_aval}"
    dataResp = apiResponse(request, urlResp, 'GET')

    trimestres = defaultdict(dict)

    for item in dataResp:
        trimestre = item['trimestre']
        indicador = item['indicador']
        if trimestre not in trimestres:
            trimestres[trimestre]['colaborador'] = item['colaborador']
            trimestres[trimestre]['indicador'] = 0
            trimestres[trimestre]['resposta'] = 0
            trimestres[trimestre]['tp_aval'] = 0
            trimestres[trimestre]['it_indic'] = defaultdict(int)
        trimestres[trimestre]['indicador'] += indicador
        trimestres[trimestre]['resposta'] += item['resposta']
        trimestres[trimestre]['tp_aval'] += item['tp_aval']
        trimestres[trimestre]['it_indic'][indicador] += item['resposta']
    pprint.pprint(trimestres)
    trimestres2 = []

    # Iterando sobre os itens do dicionário
    for valor in trimestres.values():
        trimestre = list(valor['it_indic'].values())
        trimestres2.append(trimestre)
            
    pprint.pprint(trimestres2)

    if request.method == 'POST':
        print(f'Avaliado:{dataUsuarios["nome"]}')
        for item in dataItem:
            for indicador in dataInd:
                if item['indicador'] == indicador['id']:
                    indic_id  = indicador["id"]
                    item_id  = item["id"]
                    data_resp = {
                        "colaborador": id_usuario,
                        "tp_aval":id_aval,
                        "indicador": indic_id,
                        "it_indic": item_id,
                    }
                    resp_tri = request.POST.get('res_tri{}'.format(item_id))

                    if resp_tri is not None:
                        data_resp["resposta"] = resp_tri
                        data_resp["trimestre"] = id_trimestre 
                        responseresp = requests.post(url=urlResp2, data=data_resp, headers=headers)
                        data20  = responseresp.json()
                        print(data20)
 
                    print('====================================================')
                    print(indicador['titulo'])
                    print(item['item'])
                    print(f'Trimestre é:{resp_tri}')

                    print('====================================================')
        return redirect(f'/prontocardio/prontogestao/avDesGeralFinal/{id_usuario}')

    data_ind=json.dumps(dataInd)
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'usuario_nome':dataUsuarios,
        'indicadores': dataInd,
        'itemindicador': dataItem,
        'respostas':dataResp,
        'trim':dataTrimestre,
        'usuario':id_usuario,
        'data_json':data_ind
    }
    for j in range(4):
        for i in range(12):
            try:
                value = trimestres2[j][i]
            except IndexError:
                value = 0
            context[f'tri_{j+1}_{i}'] = value
    
    return render (request, 'avCompetencia.html', context)

#=====================AUTO-AVALIAÇÃO DE COMPETENCIA===============================#
def autoAvCompetencia(request, id_usuario, id_aval, id_trimestre):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    urlUsuarios = f"http://192.168.4.33:8000/usuarios/{id_usuario}/"
    urlInd = f"http://192.168.4.33:8000/prontogestao/indicadores/?tp_aval={id_aval}"
    urlItem = f"http://192.168.4.33:8000/prontogestao/itemindicador/?tp_aval={id_aval}"
    urlResp2 = f"http://192.168.4.33:8000/prontogestao/resultado/"
    urltrim = f"http://192.168.4.33:8000/prontogestao/trimestre/{id_trimestre}/"
    
    #Indicadores
    dataInd = apiResponse(request, urlInd, 'GET')
    #Itens(Perguntas)
    dataItem = apiResponse(request, urlItem, 'GET')
    #Usuarios
    dataUsuarios = apiResponse(request, urlUsuarios, 'GET')
    #Trimestre
    dataTrimestre = apiResponse(request, urltrim, 'GET')

    dataResp = apiResponse(request, f'http://192.168.4.33:8000/prontogestao/resultado/?colaborador={id_usuario}&tp_aval={id_aval}', 'GET')

    trimestres = defaultdict(dict)

    for item in dataResp:
        trimestre = item['trimestre']
        indicador = item['indicador']
        if trimestre not in trimestres:
            trimestres[trimestre]['colaborador'] = item['colaborador']
            trimestres[trimestre]['indicador'] = 0
            trimestres[trimestre]['resposta'] = 0
            trimestres[trimestre]['tp_aval'] = 0
            trimestres[trimestre]['it_indic'] = defaultdict(int)
        trimestres[trimestre]['indicador'] += indicador
        trimestres[trimestre]['resposta'] += item['resposta']
        trimestres[trimestre]['tp_aval'] += item['tp_aval']
        trimestres[trimestre]['it_indic'][indicador] += item['resposta']
    pprint.pprint(trimestres)
    trimestres2 = []

    # Iterando sobre os itens do dicionário
    for valor in trimestres.values():
        trimestre = list(valor['it_indic'].values())
        trimestres2.append(trimestre)
            
    pprint.pprint(trimestres2)

    if request.method == 'POST':
        print(f'Avaliado:{dataUsuarios["nome"]}')
        for item in dataItem:
            for indicador in dataInd:
                if item['indicador'] == indicador['id']:
                    indic_id  = indicador["id"]
                    item_id  = item["id"]
                    data_resp = {
                        "colaborador": id_usuario,
                        "tp_aval":id_aval,
                        "indicador": indic_id,
                        "it_indic": item_id,
                    }
                    resp_tri = request.POST.get('res_tri{}'.format(item_id))

                    if resp_tri is not None:
                        data_resp["resposta"] = resp_tri
                        data_resp["trimestre"] = id_trimestre 
                        responseresp = requests.post(url=urlResp2, data=data_resp, headers=headers)
                        data20  = responseresp.json()
                        print(data20)
 
                    print('====================================================')
                    print(indicador['titulo'])
                    print(item['item'])
                    print(f'Trimestre é:{resp_tri}')

                    print('====================================================')
        return redirect(f'/prontocardio/prontogestao/avDesGeralFinal/{id_usuario}')

    data_ind=json.dumps(dataInd)
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'usuario_nome':dataUsuarios,
        'indicadores': dataInd,
        'itemindicador': dataItem,
        'respostas':dataResp,
        'trim':dataTrimestre,
        'usuario':id_usuario,
        'data_json':data_ind
    }
    for j in range(4):
        for i in range(12):
            try:
                value = trimestres2[j][i]
            except IndexError:
                value = 0
            context[f'tri_{j+1}_{i}'] = value
    
    return render (request, 'autoAvCompetencia.html', context)

def fichaColabAuto(request):
    id_user = request.session.get('id_usuario')
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
    
    dataUsuarios = apiResponse(request, f'http://192.168.4.33:8000/usuarios/{id_user}/', 'GET')
    dataCargos = apiResponse(request, urlCargos, 'GET')
    dataEscolaridade = apiResponse(request, urlEscolaridade, 'GET')

    dataAbertura = dataUsuarios['admissao']
    dataAbertura = dataAbertura[0:10]
    dataUsuarios['admissao'] = dataAbertura

    dataAbertura = dataUsuarios['admissao']
    data_objeto = datetime.datetime.fromisoformat(dataAbertura)
    data_formatada = data_objeto.strftime("%d/%m/%Y")
    dataUsuarios['admissao'] = data_formatada
    mes_da_resposta = dataUsuarios['admissao'][:10]
    dataUsuarios['admissao'] = mes_da_resposta

    for cargo in dataCargos:
        if cargo['id'] == dataUsuarios['funcao']:
            print(dataUsuarios['funcao'])
            dataUsuarios['funcao'] = cargo['nome']

    for escolaridade in dataEscolaridade:
        if escolaridade['id'] == dataUsuarios['escolaridade']:
            print(dataUsuarios['escolaridade'])
            dataUsuarios['escolaridade'] = escolaridade['nome']

    print(dataUsuarios)
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'usuario_nome':dataUsuarios,        
    }
    return render(request, 'ficha-colab-auto.html', context)

#=====================CADASTRO DE METAS DE PRODUTIVIDADE================================#
def cadastroMetasProdutividade(request, id_usuario):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result
   
    dataUsuarios = apiResponse(request, f'http://192.168.4.33:8000/usuarios/{id_usuario}/', 'GET')
    dataMetas = apiResponse(request, urlMetas, 'GET')
    dataMetasFilt = apiResponse(request, f'http://192.168.4.33:8000/prontogestao/metaGesProd/?colaborador={id_usuario}', 'GET')
    dataMetaProj = apiResponse(request, 'http://192.168.4.33:8000/prontogestao/metaProj/', 'GET')


    #=========tratativa de data para select de metas =========#
    now = datetime.datetime.now()
    current_year = now.year

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Define o locale para português brasileiro

    months = []
    for month_number in range(1, 13):
        month_name = calendar.month_name[month_number].capitalize().lower()
        month_value = f"{current_year}-{month_number:02d}-01"
        months.append({'label': month_name, 'value': month_value})
    meses = [month['label'] for month in months]
    #=========================================================#
    for item in dataMetaProj:
        dt_mes_meta = item['dt_mes_meta']
        month = datetime.datetime.strptime(dt_mes_meta, '%Y-%m-%d').strftime('%B')
        item['dt_mes_meta'] = month

    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'META_ALT':
            meta = request.POST['n_meta']
            id_meta = request.POST['id_meta']
            body_dimensao = {
                "meta": meta
            }

            urldimensao = f'http://192.168.4.33:8000/prontogestao/metaGesProd/{id_meta}/'
            responseMeta = requests.put(url=urldimensao, data=body_dimensao, headers=headers)
            dataMeta = responseMeta.json()
            print(dataMeta)
            return redirect(request.path)
        elif '_method' in request.POST and request.POST['_method'] == 'ADD_META':
            meta = request.POST['n_meta']
            body_dimensao = {
                "meta": meta,
                "colaborador": id_usuario
            }
            urldimensao = f'http://192.168.4.33:8000/prontogestao/metaGesProd/'
            responseMeta = requests.post(url=urldimensao, data=body_dimensao, headers=headers)
            dataMeta = responseMeta.json()
            print(dataMeta)
            return redirect(request.path)
        elif '_method' in request.POST and request.POST['_method'] == 'DEL_META':
            id_meta = request.POST['id_meta']

            urldimensao = f'http://192.168.4.33:8000/prontogestao/metaGesProd/{id_meta}/'
            responsedel = requests.delete(url=urldimensao, headers=headers)
            return redirect(request.path)
        elif '_method' in request.POST and request.POST['_method'] == 'META_PROJ':
            btn_del = request.POST.get('btn_delete')
            id_meta_proj = request.POST.get('id_meta_proj')
            id_meta = request.POST.get('id_meta')
            n_proj = request.POST.get('n_meta_proj')

            if btn_del == 'on':
                # Executa esta parte quando o checkbox estiver marcado
                # urlMetaProj = f'http://192.168.4.33:8000/prontogestao/metaProj/{id_meta_proj}/'
                # responsedel = requests.delete(url=urlMetaProj, headers=headers)
                # print(responsedel)
                print('Apagado')
            else:
                # Executa esta parte quando o checkbox não estiver marcado
                if btn_del is not None:
                    # Tratamento de erro: O valor de btn_del não é igual a 'on'
                    #Executa esta parte quando o checkbox estiver marcado
                    urlMetaProj = f'http://192.168.4.33:8000/prontogestao/metaProj/{id_meta_proj}/'
                    responsedel = requests.delete(url=urlMetaProj, headers=headers)
                    print(responsedel)
                    print('Apagado')
                else:
                    body = {
                        "id_meta": id_meta
                    }
                    if n_proj is not None:
                        body["vl_projetado"] = n_proj

                    urldimensao = f'http://192.168.4.33:8000/prontogestao/metaProj/{id_meta_proj}/'
                    responseMeta = requests.put(url=urldimensao, data=body, headers=headers)
                    dataMeta = responseMeta.json()
                    print(dataMeta)

            return redirect(request.path)
        elif '_method' in request.POST and request.POST['_method'] == 'META_ADD_PROJ':
            id_meta = request.POST['id_meta']
            mes_ano = request.POST['mes_ano']
            n_meta = request.POST['n_meta']
            body_dimensao = {
                "vl_projetado": n_meta,
                "dt_mes_meta": mes_ano,
                "id_meta": id_meta
            }
            urldimensao = f'http://192.168.4.33:8000/prontogestao/metaProj/'
            responseMeta = requests.post(url=urldimensao, data=body_dimensao, headers=headers)
            dataMeta = responseMeta.json()
            print(dataMeta)
            return redirect(request.path)
        else:
            print('Erro POST')

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'usuario':dataUsuarios,
        'metas':dataMetasFilt,
        'months': months,
        'projetados':dataMetaProj,
        'meses':meses
    }
    return render (request, 'cad-metas-produtividade.html', context)

#=====================LANÇAMENTO DE METAS (GESTOR)================================#
def lancMetaProdut(request):
    
    
    print(urlMetaReal)
    headers = request.session.get('headers')
    id_usuario = request.session.get('id_usuario')
    result = verifica_headers(request, headers)
    if result:
        return result

    dataMetas = apiResponse(request, f'http://192.168.4.33:8000/prontogestao/metaGesProd/?colaborador={id_usuario}', 'GET')
    dataMetasFilt = apiResponse(request, f'http://192.168.4.33:8000/prontogestao/metaGesProd/?colaborador={id_usuario}', 'GET')
    dataMetaReal = apiResponse(request, urlMetaReal, 'GET')
    print('Acima do metaproj')
    dataMetaProj = apiResponse(request, f'http://192.168.4.33:8000/prontogestao/metaProj/', 'GET')
    print('Abaixo do metaproj')


    #=========tratativa de data para select de metas =========#
    now = datetime.datetime.now()
    current_year = now.year

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Define o locale para português brasileiro

    months = []
    for month_number in range(1, 13):
        month_name = calendar.month_name[month_number].capitalize().lower()
        month_value = f"{current_year}-{month_number:02d}-01"
        months.append({'label': month_name, 'value': month_value})
    meses = [month['label'] for month in months]
    #=========================================================#
    
    
    for item in dataMetaProj:
        dt_mes_meta = item['dt_mes_meta']
        month = datetime.datetime.strptime(dt_mes_meta, '%Y-%m-%d').strftime('%B')
        item['dt_mes_meta'] = month
    
    if request.method == "POST":
        if '_method' in request.POST and request.POST['_method'] == 'PROJ_REAL':
            btn_del = request.POST.get('btn_delete')
            id_meta_real = request.POST.get('id_projetadoreal')
            n_proj = request.POST.get('n_meta_proj')
            if btn_del == 'on':
                print('Apagado')
            else:
                # Executa esta parte quando o checkbox não estiver marcado
                if btn_del is not None:
                    # Tratamento de erro: O valor de btn_del não é igual a 'on'
                    #Executa esta parte quando o checkbox estiver marcado
                    urlMetaProj = f'http://192.168.4.33:8000/prontogestao/metaReal/{id_meta_real}/'
                    responsedel = requests.delete(url=urlMetaProj, headers=headers)
                    print(responsedel)
                    print('Apagado')
                else:
                    body = {}
                    if n_proj is not None:
                        body["vl_produzido"] = n_proj
                    urldimensao = f'http://192.168.4.33:8000/prontogestao/metaReal/{id_meta_real}/'
                    responseMeta = requests.put(url=urldimensao, data=body, headers=headers)
                    dataMeta = responseMeta.json()
                    print(dataMeta)
            return redirect(request.path)
        elif '_method' in request.POST and request.POST['_method'] == 'ADD_LANC':
            meta_proj = request.POST.get('meta_proj')
            meta_real = request.POST.get('meta_real')
            body = {
                "vl_produzido": meta_real,
                "meta_proj": meta_proj,
                "colaborador": id_usuario
            }
            responseMetaReal = requests.post(url=urlMetaReal, data=body, headers=headers)
            dataMetaReal = responseMetaReal.json()
            print(dataMetaReal)
            return redirect(request.path)
        else:
            print('Else') 
    
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'metas':dataMetasFilt,
        'months': months,
        'projetados':dataMetaProj,
        'meses':meses,
        'projReal':dataMetaReal
    }
    
    return render(request, 'lancMetaProd.html', context)

#======================RESULTADO PROJEÇÃO X REAL===================================#
def resultadoLanc(request):
    headers = request.session.get('headers')
    id_usuario = request.session.get('id_usuario')
    result = verifica_headers(request, headers)
    if result:
        return result

    dataMetas = apiResponse(request, f'http://192.168.4.33:8000/prontogestao/metaGesProd/?colaborador={id_usuario}', 'GET')
    dataMetasFilt = apiResponse(request, f'http://192.168.4.33:8000/prontogestao/metaGesProd/?colaborador={id_usuario}', 'GET')
    dataMetaProj = apiResponse(request, 'http://192.168.4.33:8000/prontogestao/metaProj/', 'GET')
    dataMetaReal = apiResponse(request, urlMetaReal, 'GET')

    #=========tratativa de data para select de metas =========#
    now = datetime.datetime.now()
    current_year = now.year

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Define o locale para português brasileiro

    months = []
    for month_number in range(1, 13):
        month_name = calendar.month_name[month_number].capitalize().lower()
        month_value = f"{current_year}-{month_number:02d}-01"
        months.append({'label': month_name, 'value': month_value})
    meses = [month['label'] for month in months]
    pprint.pprint(meses)
    for item in dataMetaProj:
        dt_mes_meta = item['dt_mes_meta']
        month = datetime.datetime.strptime(dt_mes_meta, '%Y-%m-%d').strftime('%B')
        item['dt_mes_meta'] = month
    #=========================================================#
    lista_porc = []

    for projetado in dataMetaProj:
        for projReal in dataMetaReal:
            for meta in dataMetas:
                if meta['id'] == projetado['id_meta'] and projetado['id'] == projReal['meta_proj']:
                    vlr_proj = projetado["vl_projetado"]
                    vlr_real = projReal["vl_produzido"]
                    mes_proj = projetado["dt_mes_meta"]
                    meta = int(meta["id"])
                    porcentagem = (vlr_real / vlr_proj) * 100
                    porcentagem_reduzida = str(int(porcentagem))
                    #print(f'Meta:{meta["meta"]}, Porcentagem: {porcentagem_reduzida}%')
                    lista_porc.append({'porcentagem': porcentagem_reduzida, 'mes': mes_proj, 'meta':meta, 'projetado':vlr_proj, 'lancado':vlr_real})
    
    mapped_data = {}
    for item in lista_porc:
        meta_id = item['meta']
        if meta_id not in mapped_data:
            mapped_data[meta_id] = {'lancados': [], 'projetados': []}
        mapped_data[meta_id]['lancados'].append(item['lancado'])
        mapped_data[meta_id]['projetados'].append(item['projetado'])
    
    print('========================================')
    print('Porcentagem calculada')
    pprint.pprint(lista_porc)
    print('========================================')

    pprint.pprint(mapped_data)
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'meses':meses,
        'metas':dataMetasFilt,
        'resultados':lista_porc,
        'dados': mapped_data,
    }
    return render(request, 'resultado_lancamentos.html', context) 

def resultadoLancv2(request, id_usuario):
    headers = request.session.get('headers')
    result = verifica_headers(request, headers)
    if result:
        return result

    dataMetas = apiResponse(request, f'http://192.168.4.33:8000/prontogestao/metaGesProd/?colaborador={id_usuario}', 'GET')
    dataMetasFilt = apiResponse(request, f'http://192.168.4.33:8000/prontogestao/metaGesProd/?colaborador={id_usuario}', 'GET')
    dataMetaProj = apiResponse(request, 'http://192.168.4.33:8000/prontogestao/metaProj/', 'GET')
    dataMetaReal = apiResponse(request, urlMetaReal, 'GET')

    #=========tratativa de data para select de metas =========#
    now = datetime.datetime.now()
    current_year = now.year

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Define o locale para português brasileiro

    months = []
    for month_number in range(1, 13):
        month_name = calendar.month_name[month_number].capitalize().lower()
        month_value = f"{current_year}-{month_number:02d}-01"
        months.append({'label': month_name, 'value': month_value})
    meses = [month['label'] for month in months]
    print(meses)
    for item in dataMetaProj:
        dt_mes_meta = item['dt_mes_meta']
        month = datetime.datetime.strptime(dt_mes_meta, '%Y-%m-%d').strftime('%B')
        item['dt_mes_meta'] = month
    #=========================================================#
    lista_porc = []
    

    for projetado in dataMetaProj:
        for projReal in dataMetaReal:
            for meta in dataMetas:
                if meta['id'] == projetado['id_meta'] and projetado['id'] == projReal['meta_proj']:
                    vlr_proj = projetado["vl_projetado"]
                    vlr_real = projReal["vl_produzido"]
                    mes_proj = projetado["dt_mes_meta"]
                    meta = int(meta["id"])
                    porcentagem = (vlr_real / vlr_proj) * 100
                    porcentagem_reduzida = str(int(porcentagem))
                    #print(f'Meta:{meta["meta"]}, Porcentagem: {porcentagem_reduzida}%')
                    lista_porc.append({'porcentagem': porcentagem_reduzida, 'mes': mes_proj, 'meta':meta})

    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'meses':meses,
        'metas':dataMetasFilt,
        'resultados':lista_porc
    }
    return render(request, 'resultado_lancamentos.html', context) 
#==================================================================================#
