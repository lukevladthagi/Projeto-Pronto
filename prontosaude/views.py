from django.shortcuts import render

#=====================PRONTOSAUDE==============================#
def consultaPaciente(request):
    if request.method == 'POST':
        return render (request, 'resultado-paciente.html')
    return render (request, 'consulta-paciente.html')
def pacienteResupesquisa(request):
    aaa = 10
    context = {
        'teste':aaa
    }
    return render (request, 'paciente-resupesquisa.html', context)
