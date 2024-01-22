from datetime import datetime
from dateutil.parser import isoparse
import requests, json, pprint, pytz
from django.http import JsonResponse

#========================= Função Auxiliar Checklist =========================#
def substituir_codigo(request, usuario, usuario2):
    # Atualize o campo local_id em array1 com base no mapeamento
    for item in usuario:
        for item2 in usuario2:
            if item['codigo'] == item2['id']:
                item['codigo'] = item2['username']

    # Retorne o array1 atualizado como uma resposta JSON
    return array
    
#==================================================================================#