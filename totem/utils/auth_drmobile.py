import requests

def authDrMobile(request):
    url = "https://api.drmobile.com.br:9443/prontocardio/auth/"
    auth_body = {
        "email": "prontocardio@drmobile.com.br",
        "senha": "H0sp1t@lPr0nt0C4rd10@"
    }

    response = requests.post(url=url,json=auth_body)
    data = response.json()
    tp_token = data['tipo']
    tk = data['token']
    token = f"{tp_token} {tk}"
    return token

def apiResponseDrMobile(request, token, urlReceived, requestType, data=None, file=None):
    headers = {'Authorization' : token}
    #print(headers)
    try:
        if requestType == 'GET':
            print('get', headers, urlReceived)
            response = requests.get(url=urlReceived, headers=headers)
            print(response.status_code)
        elif requestType == 'POST':
            response = requests.post(url=urlReceived, json=data,headers=headers)
            print(response.status_code)
            print(data, 'DATA RECEBIDA')
        elif requestType == 'PUT':
            #print('Put feito')
            response = requests.put(url=urlReceived, data=data, headers=headers)
            status = response.status_code
        elif requestType == 'DEL':
            response = requests.delete(url=urlReceived, headers=headers)
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

