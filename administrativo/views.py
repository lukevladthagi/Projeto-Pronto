from tokenize import String
from django.shortcuts import render, redirect
import requests, json, pprint, pytz
from datetime import datetime, timezone
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
host = "192.168.4.33:8000"
setor = f"http://{host}/setores/"
def login(request):
    if request.method == 'POST':
        # ------Pega usuario e senha------#
        username = request.POST.get('username')
        request.session['cod_usuario'] = username
        password = request.POST.get('password')
        # --------------------------------#
        urlLogin = f'http://{host}/api/login/'
        urlUsers = f'http://{host}/users/?username={username}'

        user_login = {
            "username": f'{username}',
            "password": f'{password}'
        }
        
        responseLogin = requests.post(url=urlLogin, json=user_login)
        pprint.pprint(responseLogin.json())
        if responseLogin.status_code == 200:
            data = responseLogin.json()
            tptoken = 'token'
            tk = data['token']
            token = f"{tptoken} {tk}"
            headers = {'Authorization': token}
            request.session['headers'] = headers
            request.session['token'] = token
            
            responseUsers = requests.get(url=urlUsers, headers=headers)
            dataUser = responseUsers.json()
            for User in dataUser:
                urlUsuarios = f'http://{host}/usuarios/?codigo={User["id"]}'
                responseUsuarios = requests.get(url=urlUsuarios, headers=headers)
                dataUsuarios = responseUsuarios.json()
                pprint.pprint(dataUsuarios)
                request.session['nm_colaborador'] = dataUsuarios[0]['nome']
                request.session['id_usuario'] = dataUsuarios[0]["id"]
                request.session['id_setor'] = User['groups']
            return redirect("/prontocardio/")
        else:
            mensagem_tipo = 'danger'
            mensagem = 'Usuário ou senha Incorreta'
            # Password is incorrect, add an error message
            #messages.error(request, 'Incorrect password. Please try again.')
            context = {
                'mensagem_tipo':mensagem_tipo,
                'mensagem':mensagem
            }
            return render(request, 'login.html', context)
    return render(request, 'login.html')

def loginChamados(request):
    if request.method == 'POST':
        # ------Pega usuario e senha------#
        username = request.POST.get('username')
        request.session['cod_usuario'] = username
        password = request.POST.get('password')
        # --------------------------------#
        urlLogin = f'http://{host}/api/login/'
        urlUsers = f'http://{host}/users/?username={username}'

        user_login = {
            "username": f'{username}',
            "password": f'{password}'
        }
        responseLogin = requests.post(url=urlLogin, json=user_login)
        pprint.pprint(responseLogin.json())
        if responseLogin.status_code == 200:
            data = responseLogin.json()
            tptoken = 'token'
            tk = data['token']
            token = f"{tptoken} {tk}"
            headers = {'Authorization': token}
            request.session['headers'] = headers
            request.session['token'] = token
            
            responseUsers = requests.get(url=urlUsers, headers=headers)
            dataUser = responseUsers.json()
            for User in dataUser:
                urlUsuarios = f'http://{host}/usuarios/?codigo={User["id"]}'
                responseUsuarios = requests.get(url=urlUsuarios, headers=headers)
                dataUsuarios = responseUsuarios.json()
                pprint.pprint(dataUsuarios)
                request.session['nm_colaborador'] = dataUsuarios[0]['nome']
                request.session['id_usuario'] = dataUsuarios[0]["id"]
                request.session['id_setor'] = User['groups']
            return redirect("/prontocardio/prontoticket/abrir_chamado_usuario/")
        else:
            mensagem_tipo = 'danger'
            mensagem = 'Usuário ou senha Incorreta'
            # Password is incorrect, add an error message
            #messages.error(request, 'Incorrect password. Please try again.')
            context = {
                'mensagem_tipo':mensagem_tipo,
                'mensagem':mensagem
            }
            return render(request, 'login.html', context)
    return render(request, 'login.html')
    
def logout(request):
    headers = request.session.get('headers')
    print(headers)

    url = 'http://192.168.4.33:8000/api/logout/'
    try:
        response = requests.delete(url, headers=headers)
        # Verificar se o logout foi bem-sucedido (200 OK)
        if response.status_code == 200:
            print("Logout realizado com sucesso.")
            request.session['headers'] = None
            return redirect("/prontocardio/login")
        else:
            print(f"Falha ao fazer logout. Status code: {response.status_code}")
            print(response.json())
            return redirect("/prontocardio/login")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
        return HttpResponse(f"Erro ao fazer a requisição: {e}", status=500)

def resetaSenha(request):
    try:
        headers = request.session.get('headers')
        bloq_tela = request.session.get('id_setor')

        if not headers:
            return render(request, 'pages-error-404.html')

        if request.method == 'POST':
            senhaAnterior = request.POST.get('currentpassword')
            senhaAtual = request.POST.get('newpassword')

            passwordBody = {
                'old_password': senhaAnterior,
                'new_password': senhaAtual
            }

            passwordChange = apiResponse(request, f'http://{host}/api/change-password/', 'PUT', data=passwordBody)
            print(f'passwordChange: {passwordChange}')  # Added print statement

            if passwordChange['code'] == 400:
                status = 'danger'
            elif passwordChange['code'] == 200:
                status = 'success'
            else:
                # Handle other status codes if needed
                status = 'danger'

            context = {
                'bloq_tela': bloq_tela,
                'nm_colaborador': request.session.get('nm_colaborador'),
                'mensagem': passwordChange['message'],
                'mensagem_tipo': status
            }
            print(f'context: {context}')  # Added print statement
            return render(request, 'reseta-senha.html', context)

    except Exception as e:
        # Handle any exceptions that might occur
        print(f"An error occurred: {e}")
        context = {
            'bloq_tela': bloq_tela,
            'nm_colaborador': request.session.get('nm_colaborador'),
            'mensagem': 'An error occurred while processing your request.',
            'mensagem_tipo': 'danger'
        }
        print(f'context: {context}')  # Added print statement
        return render(request, 'reseta-senha.html', context)
    #================== ARQUIVOS JSONS ==========================#
    data_setor = apiResponse(request,setor, 'GET' )
    #============================================================#
    
    resultado = []            
    for valor in bloq_tela:
        setor_encontrado = next((setor for setor in data_setor if setor['id'] == valor), None)
        if setor_encontrado:
            resultado.append(setor_encontrado)
    print(resultado)            
    context = {
        'bloq_tela': bloq_tela,
        'nm_colaborador': request.session.get('nm_colaborador'),
        'set_usuario':resultado
    }
    return render(request, 'reseta-senha.html',context)


def telaInicial(request):
    headers = request.session.get('headers')
    # URL que você deseja renderizar dentro do seu template
    url = "http://192.168.4.3/intranet/"

    response = requests.get(url)
    # Verifique se a resposta foi bem-sucedida
    response.raise_for_status()

    # Renderize o conteúdo da resposta no template
    content = response.text
    if not headers:
        return render(request, 'pages-error-404.html')
    context = {
        'bloq_tela':request.session.get('id_setor'),
        'nm_colaborador':request.session.get('nm_colaborador'),
        'content': content,
    }
    return render(request, 'tela_inicial.html', context)   

def formataData(dataAbertura, dataAlteracao=None, formato=None):
        dataAbertura = str(dataAbertura)
        dataAlteracao = str(dataAlteracao)

        br_tz = pytz.timezone('America/Sao_Paulo')
        utc_abertura = datetime.strptime(dataAbertura, formato) 
        utc_abertura = pytz.utc.localize(utc_abertura)
        br_abertura = utc_abertura.astimezone(br_tz)
        dateChamado = br_abertura.strftime("%d/%m/%Y, %H:%M")

        utcAlteracao = datetime.strptime(dataAlteracao, formato)
        utcAlteracao = pytz.utc.localize(utcAlteracao)
        brAlteracao = utcAlteracao.astimezone(br_tz)
        alteracaoChamado = brAlteracao.strftime("%d/%m/%Y, %H:%M")

        return dateChamado, alteracaoChamado

#Converte o formato ISO em datetime
def converter_data(data_string):
    formato = "%Y-%m-%dT%H:%M:%S.%fZ"
    data_string = str(data_string)

    br_tz = pytz.timezone('America/Sao_Paulo')
    utc_abertura = datetime.strptime(data_string, formato) 
    utc_abertura = pytz.utc.localize(utc_abertura)
    br_abertura = utc_abertura.astimezone(br_tz)
    dateChamado = br_abertura.strftime("%d/%m/%Y, %H:%M")

    return dateChamado

#Calcula o tempo corrido
def calcular_diferenca_tempo(data_inicio):
    data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    data_atual = datetime.now(timezone.utc)

    diferenca = data_atual - data_inicio_dt

    dias = diferenca.days
    segundos_totais = diferenca.seconds
    horas, segundos_totais = divmod(segundos_totais, 3600)
    minutos, segundos = divmod(segundos_totais, 60)

    if dias == 1:
        diferenca_formatada = f"{dias} Dia, {horas:02d}:{minutos:02d}:{segundos:02d}"
    else:
        diferenca_formatada = f"{dias} Dias, {horas:02d}:{minutos:02d}:{segundos:02d}"

    return diferenca_formatada

#calcula o tempote entre created e update
def calcular_tempo_entre_created_updated(objeto):
    created_at = objeto.get('created_at')
    updated_at = objeto.get('updated_at')

    if created_at and updated_at:
        try:
            created_at_dt = datetime.fromisoformat(created_at)
            updated_at_dt = datetime.fromisoformat(updated_at)
            print('============================')
            print('============================')
            diferenca = updated_at_dt - created_at_dt

            dias = diferenca.days
            segundos_totais = diferenca.seconds
            horas, segundos_totais = divmod(segundos_totais, 3600)
            minutos, segundos = divmod(segundos_totais, 60)

            if dias == 1:
                diferenca_formatada = f"{dias} Dia, {horas:02d}:{minutos:02d}:{segundos:02d}"
            else:
                diferenca_formatada = f"{dias} Dias, {horas:02d}:{minutos:02d}:{segundos:02d}"

            return diferenca_formatada
        except ValueError:
            # Lidar com datas em um formato inválido
            return "Datas em formato inválido"
    else:
        return None

#Insere no creted_At data e hora atual
def obter_data_hora_formatada():
    # Obtendo a data e hora atual formatada
    data_hora_atual = datetime.now()
    data_hora_formatada = data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')
    return data_hora_formatada

# Retorna a response do determinado endpoint que vai ser acessado
def apiResponse(request, urlReceived, requestType, data=None, file=None):
    headers = request.session.get('headers')
    try:
        if requestType == 'GET':
            response = requests.get(url=urlReceived, headers=headers)
        elif requestType == 'POST':
            response = requests.post(url=urlReceived, data=data, files=file, headers=headers)
            print(response.status_code)
        elif requestType == 'PUT':
            print('Put feito')
            response = requests.put(url=urlReceived, data=data, files=file, headers=headers)
            status = response.status_code
        elif requestType == 'DEL':
            print('Função deletar ativada')
            response = requests.delete(url=urlReceived, headers=headers)
            print(response)
        else:
            return None  # Tipo de requisição inválido

        status = response.status_code
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

def render_error_404(request):
    return render(request, 'pages-error-404.html')

def verifica_headers(request, headers):
    dataset = apiResponse(request, f'http://{host}/prontocheck/setor/', 'GET')

    if not headers:
        return render(request, 'pages-error-404.html')
    elif 'detail' in dataset:
        return render(request, 'token_expirado.html')
    else:
        pass
