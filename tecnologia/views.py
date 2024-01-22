from django.shortcuts import render
from administrativo.views import apiResponse, host, render_error_404
from .utils import *

# Create your views here.
urlUsuarios = f"http://{host}/usuarios/"
urlUsers = f"http://{host}/users/"


def listar_usuario(request):
    dataUsuarios = apiResponse(request, urlUsuarios, 'GET')
    dataUsers = apiResponse(request, urlUsers, 'GET')
    for item in dataUsuarios:
        for item2 in dataUsers:
            if item['codigo'] == item2['id']:
                item['codigo'] = item2['username']
                if item2['password']:
                    item['acesso'] = True
                else:
                    item['acesso'] = False
    if request.method == "POST":
        id_usuario = request.POST.get('id_usuario')
        print(id_usuario)
    context = {
        'bloq_tela': request.session.get('id_setor'),
        'nm_colaborador': request.session.get('nm_colaborador'),
        'usuarios': dataUsuarios,
    }
    return render(request, 'listar_usuario.html', context)
