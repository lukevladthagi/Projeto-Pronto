from django.shortcuts import render, redirect
import requests, pprint, json, time
from datetime import datetime
from datetime import date
from .utils.auth_drmobile import authDrMobile, apiResponseDrMobile
#from utils import auth_drmobile

def login(request):

    #Apagando a sessão que guarda os exames agendados
    reset_sessao(request)

    if request.method == 'POST':
        data = request.POST.get('data')
        request.session['token'] = authDrMobile(request)
        request.session['cpf'] = request.POST.get('cpf')
        token = request.session.get('token')
        cpf = request.session.get('cpf') 

        usuario = apiResponseDrMobile(request, token, f'https://api.drmobile.com.br:9443/prontocardio/paciente/cpf/{cpf}', 'GET')

        request.session['nrCelular'] = usuario['nrCelular']
        request.session['cdPaciente'] = usuario['cdPaciente']
        request.session['tpSexo'] = usuario['tpSexo']

        print(usuario)
        
        if usuario != '':
            #Calculo da idade
            dt = str(data).split("-")
            dt.reverse()
            request.session['dataNasc'] = '-'.join(dt).replace("-", "/")
            anoAtual = int(date.today().year)
            mesAtual = int(date.today().month)
            diaAtual = int(date.today().day)
            ano = int(data[6:10])
            mes = int(data[3:4])
            dia = int(data[0:1])
            request.session['idadeIni'] = anoAtual - ano - ((mesAtual, diaAtual) < (mes, dia))
            carteira = usuario['carteira']
            return verifica_carteira(carteira)
        
        else:
            #TODO: 'criar tratativa para caso não exista o cpf no sistema'
            pass

    return render(request, 'loginTotem.html')

def verifica_carteira(carteira):
    
    if carteira:
        return redirect("/totem/marcacao/")

    else:
        return redirect("/totem/informaConvenio/")
    
#Escolhe o tipo de paciente: Sou paciente ou novo paciente
def paciente(request):
    return render(request,'tipoPaciente.html')

#Tela após clicar em novo paciente
def novoPac(request):
    request.session['token'] = authDrMobile(request)
    token = request.session.get('token')

    dataConvenio = apiResponseDrMobile(request, token, 'https://api.drmobile.com.br:9443/prontocardio/convenios/agendamento',  'GET')
    context = {'dados': dataConvenio}

    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('DataNascimento')
        tpsexo = request.POST.get('tpsexo')
        
        request.session['cpf'] = request.POST.get('cpf')
        request.session['cd_convenio'] = request.POST.get('cd_convenio')
        request.session['nrTel'] = request.POST.get('telefone')
        request.session['email'] = request.POST.get('email')
        cpf = request.session.get('cpf')
        telefone = request.session.get('telefone')

        dt = str(data_nascimento).split("-")
        dt.reverse()
        request.session['dataNasc'] = '-'.join(dt).replace("-", "/")
        
        data_nasc = datetime.strptime(data_nascimento, "%Y-%m-%d")
        dia_atual = datetime.now()
        
        request.session['idadeIni'] = dia_atual.year - data_nasc.year - ((dia_atual.month, dia_atual.day) < (data_nasc.month, data_nasc.day))

        user_data = {
            "nome": f'{nome}',
            "nascimento": f'{data_nascimento}',
            "nrCpf": f'{cpf}',
            "tpsexo": f'{tpsexo}',
            "nrCelular": telefone
        }
        apiResponseDrMobile(request, token, 'https://api.drmobile.com.br:9443/prontocardio/cadastra/paciente', 'POST', user_data)
        return render(request, "esc_marc.html")
    
    return render(request,'cadPaciente.html', context)

#Escolhe os tipos de agendamento
def esc_Agend(request):
    return render(request, 'esc_marc.html')

#Escolha de agendamento, apos clicar em agendamento de consulta
def esc_agendamento(request):
    return render(request, 'esc_agendamento.html')

#Lista servicos disponiveise log em seguida diz horario disponivel
def servico(request):
    url = 'https://api.drmobile.com.br:9443/prontocardio/especialidades'
    token = request.session.get('token')
    headers = {
    'Authorization' : token
    }
    response = requests.get(url=url,headers=headers)
    data = response.json()
    print(data)
    context = {}
    context['dados'] = data['data']
    return render(request,'servicos.html', context)

#Mostra convenio e direciona para os exames
def convenioExa(request):
    url = 'https://api.drmobile.com.br:9443/prontocardio/convenios/agendamento'
    token = request.session.get('token')

    headers = {
    'Authorization' : token
    }

    response = requests.get(url=url,headers=headers)
    data = response.json()
    print(data)
    context = {}
    context['dados'] = data
    return render(request,'convenioExame.html', context)

#Mostra convenio e direciona para as especialidades
def convenioCons(request):
    url = 'https://api.drmobile.com.br:9443/prontocardio/convenios/agendamento'
    token = request.session.get('token')
    headers = {
    'Authorization' : token
    }
    response = requests.get(url=url,headers=headers)
    data = response.json()
    print(data)
    context = {}
    context['dados'] = data
    return render(request,'convenioConsulta.html', context)

#mostra os nomes dos prestadores
def mostraPrestador(request):
    if request.method == 'POST':
        nrPrest = request.POST.get('nrPrest')
        print(nrPrest)
    url = 'https://api.drmobile.com.br:9443/prontocardio/prestadores/16'
    token = request.session.get('token')
    headers = {
    'Authorization' : token
    }
    response = requests.get(url=url,headers=headers)
    data = response.json()
    context = {}
    context['servico'] = data
    return render(request,'prestadores.html',context)

#Mostra os exames e ao selecionar mostra os horarios disponiveis
def mostraExames(request):
    token = request.session.get('token')
    exames_data = apiResponseDrMobile(request, token, 'https://api.drmobile.com.br:9443/prontocardio/agendamento/itens/I', 'GET')
    context = {'dados': exames_data['data']}

    if request.method == 'POST':
        
        cdex = request.POST.getlist('nrServico[]')
        print('=========================================')
        print(cdex, 'CDEX')
        print('=========================================')
        nrcpf = request.session.get('cpf')
        idade = request.session.get('idadeIni')
        tpsexo = request.session.get('tpSexo')
        agendBody = request.session.get('agendBody')
        cd_convenio = request.session.get('cd_convenio')
        exames = []

        start_time = time.time()

        for item in cdex:

            user_data = {
                "cpf": str(nrcpf),
                "idade": int(idade),
                "sexo": str(tpsexo),
                "hospital": "08711085000128",
                "servico": "6",
                "convenio": cd_convenio,
                "identity": str(nrcpf),
                "item": str(item)
            }
            exame = apiResponseDrMobile(request, token, 'https://api.drmobile.com.br:9443/prontocardio/localizahorarios', 'POST', user_data)
            exames.append(exame['menuhorarios'])
            

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(elapsed_time)

        
        """ for exame in exames:
            print(exame[0]['descricao'])
            for item in exame:
                #print(item['descricao'])
                pass """
        

        request.session['exames'] = exames


        print('------------------------------')
        pprint.pprint(exames)
        print('------------------------------')

        """ exames = apiResponseDrMobile(request, token, 'https://api.drmobile.com.br:9443/prontocardio/localizahorarios', 'POST', user_data)
        request.session['exames'] = exames
        print(exames, 'EXAMES') """
       
        

        

        return redirect("/totem/agendarExames/")
        
    return render(request,'exames.html', context)

#Verificar agendamento 
def verifcarAgend(request):
    
    return render(request, "agendamentos.html")

#Cancela agendamento 
def cancelaAgenda(request):
        #Vai no html e pega o cpf informado pela pessoa
        nrcpf = request.session.get('cpf')
        print(nrcpf)
        url = f'https://api.drmobile.com.br:9443/prontocardio/paciente/cpf/{nrcpf}'
        token = request.session.get('token')
        headers = {
            'Authorization' : token
        }
        response = requests.get(url=url,headers=headers)
        data = response.json()
        print(response.status_code)
        if response.status_code == 200:
            print(response.status_code)
            print('DEU  certo')
            print(data)
            request.session['cdPaciente'] = data['cdPaciente']
            cdPac = request.session.get('cdPaciente')
            #----------------------------------------------------------------------------#
            #Pega o codigo do paciente recebido pela url anterior
            print('---------------------------------------------------------------------------------------------------')
            url2 = f'https://api.drmobile.com.br:9443/prontocardio/locagenda/{cdPac}'
           
            response2 = requests.get(url=url2,headers=headers)
            if response2.status_code == 200:

                data2 = response2.json()
                context = {}
                context['dados'] = data2['agendas']
                print(context)

                #agenda = data2['agendas']
                for item in data2['agendas']:
                    cdItAgendCent = item['cdItAgendaCentral']
                print(cdItAgendCent)
                print('---------------------------------------------------------------------------------------------------')
            else:
                context = {}
                print(context)
                print(type(context))
            #-----------------------------------------------------------------------------#
            
            print('Recebeu tudo certo')
            
            """ response3 = requests.delete(url=url3,headers=headers)
            dataf = response3.json()
            print(dataf)
            if response3.status_code > 200:
                #Tirar essa parte de pegaCpf e criar uma pagina para tratar dos erros
                print(response3.status_code)
                print('Deu erro na terceira parte')
                return render(request,'pegaCpf.html')
            data3 = response3.json()
            print(response3.status_code) 
            print(data3)"""

            return render(request,'cancelarAgend.html', context)

def cancelaExame(request):
        #Vai no html e pega o cpf informado pela pessoa
        nrcpf = request.session.get('cpf')
        print(nrcpf)
        url = f'https://api.drmobile.com.br:9443/prontocardio/paciente/cpf/{nrcpf}'
        token = request.session.get('token')

        headers = {
            'Authorization' : token
        }
        response = requests.get(url=url,headers=headers)
        data = response.json()
        print(response.status_code)
        if response.status_code == 200:
            print(response.status_code)
            print('DEU  certo')
            print(data)
            global cdPac
            cdPac = data['cdPaciente']
            #----------------------------------------------------------------------------#
            #Pega o codigo do paciente recebido pela url anterior
            print('---------------------------------------------------------------------------------------------------')
            url2 = f'https://api.drmobile.com.br:9443/prontocardio/agendamento/exames/{cdPac}'
           
            response2 = requests.get(url=url2,headers=headers)
            if response2.status_code == 200:

                data2 = response2.json()
                context = {}
                context['dados'] = data2['data']
                print(context)

                #agenda = data2['agendas']
                """ for item in data2['agendas']:
                    cdItAgendCent = item['cdItAgendaCentral'] """
                #print(cdItAgendCent)
                print('---------------------------------------------------------------------------------------------------')
            else:
                context = {}
                print(context)
                print(type(context))
            #-----------------------------------------------------------------------------#
            
            print('Recebeu tudo certo')
            
            """ response3 = requests.delete(url=url3,headers=headers)
            dataf = response3.json()
            print(dataf)
            if response3.status_code > 200:
                #Tirar essa parte de pegaCpf e criar uma pagina para tratar dos erros
                print(response3.status_code)
                print('Deu erro na terceira parte')
                return render(request,'pegaCpf.html')
            data3 = response3.json()
            print(response3.status_code) 
            print(data3)"""

            return render(request,'cancelarExame.html', context)

def agendar(request, cdopc):
    
        #Vai no html e pega o cpf e telefone informado pela pessoa
        nrcpf = request.session.get('cpf')
        nrtel = request.session.get('nrtel')
        dtNasc = request.session.get('dataNasc')
        urlConvenios = "https://api.drmobile.com.br:9443/prontocardio/convenios/agendamento"
        url = f'https://api.drmobile.com.br:9443/prontocardio/paciente/cpf/{nrcpf}'
        token = request.session.get('token')
        cd_convenio = request.session.get('cd_convenio')

        headers = {
            'Authorization' : token
        }
        response = requests.get(url=url,headers=headers)
        response2 = requests.get(url=urlConvenios, headers=headers)
        data = response.json()
        data2 = response2.json()
        print(response.status_code)
        print(data)
        for itens in data2:
            if itens['codigo_convenio'] == int(cd_convenio):
                nm_convenio = itens['nome_convenio']
        
        
        cdConv = cd_convenio
        nmConv = nm_convenio
        cdpla = 1
        nmPla = nm_convenio
        cdPac = data['cdPaciente']
        sexo = data['tpSexo']
        if response.status_code == 200:
            print(response.status_code)
            print('Deu certo')
            print("----------------")
            #----------------------------------------------------------------------------#
            #Pega o codigo do paciente recebido pela url anterior
            url2 = "https://api.drmobile.com.br:9443/prontocardio/agendamento/"

            headers2 = {
                'Authorization' : token
            }
        
            user_data = {
                "cpf": str(f"{nrcpf}"),
                "codigopaciente": str(f"{cdPac}"),
                "hospital": "08711085000128",
                "opcaohorario": str(f"{cdopc}"),
                "nmConv": f"{nmConv}",
                "celular": str(f"{nrtel}"),
                "convenio": str(f"{cdConv}"),
                "plano": str(f"{cdpla}"),
                "nmPla": f"{nmPla}",
                "nascimento": str(f"{dtNasc}"),
                "identity": str(f"{nrcpf}"),
                "sexo": f"{sexo}"
            }
            pprint.pprint(user_data)
            #response2 = requests.post(url=url2,json=user_data,headers=headers2)
            #data2 = response2.json()
            """ if response2.status_code > 200:
                print(response2.status_code)
                print(data2)
                return render
                return render_to_pdf(
                    'agendado.html',
                    {
                        'pagesize':'A4',
                        'dados': data2,
                    }
                )  """
                #context = {}
                #context['dados'] = data2
                #return render(request,'agendado.html', context)
            #pprint.pprint(data2['mensagem'])
            request.session['agendBody'] = user_data
            return redirect("/totem/confirmaAgendamento/")
        else:
            print('DEU ERRO')
            print("Error from server: " + str(response.content))

def agendarExames(request):
    
    if request.method == 'POST':
        horario = request.POST.getlist('nrHorario[]')
        print(horario)
        #return render(request, "agendadoExame.html", context)
    
    nrcpf = request.session.get('cpf')
    nrtel = request.session.get('nrCelular')
    dtNasc = request.session.get('dataNasc')
    token = request.session.get('token')
    cd_convenio = request.session.get('cd_convenio')
    cdPac = request.session.get('cdPaciente')
    sexo = request.session.get('tpSexo')


    exames = request.session.get('exames') 
    
    if exames != None:
        context_horarios = {'exames': exames}
    else:
        context_horarios = {'exames': []}

    return render(request, "examesHorarios.html", context_horarios)

def horarioConsulta(request, cdesp):
        #Vai no html e pega o cpf informado pela pessoa
        nrcpf = request.session.get('cpf')
        idade = request.session.get('idadeIni')
      
        url = f'https://api.drmobile.com.br:9443/prontocardio/paciente/cpf/{nrcpf}'
        token = request.session.get('token')
        cd_convenio = request.session.get('cd_convenio')
        
        headers = {
            'Authorization' : token
        }
        response = requests.get(url=url,headers=headers)
        data = response.json()
        print(response.status_code)
        
        if response.status_code == 200:            
            print('DEU  certo')
            pprint.pprint(data)
            sexo = data['tpSexo'] 
            #----------------------------------------------------------------------------#
            #Recebe todos os dados e localiza os horarios
            #start_time = time.time()
            url2 = 'https://api.drmobile.com.br:9443/prontocardio/localizahorarios'
            headers2 = {
                'Authorization' : token
            }
            user_data2 = {
                "cpf": str(f"{nrcpf}"),
                "idade": int(f"{idade}"),
                "sexo": str(f"{sexo}"),
                "hospital": "08711085000128",
                "servico": str(f"{cdesp}"),
                "convenio": int(f"{cd_convenio}"),
                "identity": str(f"{nrcpf}"),
            }
            #pprint.pprint(user_data2)
            responseConsulta = requests.post(url=url2,json=user_data2,headers=headers2)
            #end_time = time.time()
            #elapsed_time = end_time - start_time
            #print(elapsed_time)
            
            if responseConsulta.status_code == 200:
                data2 = responseConsulta.json()
                #pprint.pprint(data2['menuhorarios'])
                context = {}
                context['dados'] = data2['menuhorarios']
                print("MEUS HORARIOS")
                print("==========")
                print(context)
                print("==========")

            else:
                context = {}

            return render(request,'horarioConsulta.html',context)  

def informa_convenio(request):
     
    token = request.session.get('token')
    celular = request.session.get('nrCelular')
    convenio = apiResponseDrMobile(request, token, f'https://api.drmobile.com.br:9443/prontocardio/convenios/agendamento', 'GET')
    context = {'dados': convenio, 'celular': celular}
    #TODO: Passar o nrtel pra ver se esta vazio ou não, se não tiver vai aparecer o select do tel pra selecionar

    
    if request.method == 'POST':
        request.session['cd_convenio'] = request.POST.get('convenio')
        request.session['nrCelular'] = request.POST.get('telefone')
        return redirect("/totem/marcacao/")

    
    return render(request, 'informa_convenio.html', context)

def confirmaAgend(request):
    cpf = request.session.get('cpf')
    token = request.session.get('token')
    agendBody = request.session.get('agendBody')
    nrTel = request.session.get('nrCelular')
 

    headers = {
        'Authorization' : token
    }

    urlAgendamento = "https://api.drmobile.com.br:9443/prontocardio/agendamento/"
    urlpaciente = f"https://api.drmobile.com.br:9443/prontocardio/paciente/cpf/{cpf}"
    responseusuario = requests.get(url=urlpaciente,headers=headers)
    datausuario = responseusuario.json()
    nm_paciente = datausuario['nmPaciente']
    

    context = {
        'dados': agendBody,
        'nome':nm_paciente,
        'nrTel': nrTel,
    }

    print(agendBody, 'esse body')
    
    if request.method == 'POST':
        nrCpf = request.POST.get('cpf')
        tel = request.POST.get('tel')
        nmPlano = 1

        user_data = {
            "cpf": str(f"{nrCpf}"),
            "codigopaciente": str(agendBody['codigopaciente']),
            "hospital": "08711085000128",
            "opcaohorario": str(agendBody['opcaohorario']),
            "celular": tel,
            "convenio": agendBody['convenio'],
            "plano": str(f"{nmPlano}"),
            "nascimento": str(agendBody['nascimento']),
            "identity": str(agendBody['cpf']),
            "sexo": str(agendBody['sexo'])
        }

        print(user_data, 'DATA D AG')
        #print(nrCpf, nmPlano)
        
        response = requests.post(url=urlAgendamento,json=user_data,headers=headers)
        print(response.status_code, 'status')
        data = response.json()

        context2 = {}
        context2['dados'] = data
        return render(request, "agendado.html", context2)
        
        
    return render(request, "confirmaAgend.html", context)

def confirmaCancelamento(request, cdIt):
    token = request.session.get('token')
    cdPac = request.session.get('cdPaciente')
    headers = {
        'Authorization' : token
    }
    urlDelete = f'https://api.drmobile.com.br:9443/prontocardio/cancela/{cdPac}/{cdIt}'

    if request.method == 'POST':
        response = requests.delete(url=urlDelete,headers=headers)
        return redirect('/totem/cancelaagendamento/')

    return render(request, "confirmaCancelamento.html")

def confirmaCancelamentoExame(request, cdIt):
    token = request.session.get('token')
    cdPac = request.session.get('cdPaciente')
    headers = {
        'Authorization' : token
    }
    urlDelete = f'https://api.drmobile.com.br:9443/prontocardio/cancela/{cdPac}/{cdIt}'

    if request.method == 'POST':
        response = requests.delete(url=urlDelete,headers=headers)
        return redirect('/totem/cancelaExame/')
        
    return render(request, "confirmaCancelamento.html")

def reset_sessao(request):
    request.session['descricao_array'] = []
    request.session.save()