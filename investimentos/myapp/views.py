from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests

def home(request):
    return render(request, 'myapp/index.html')

@login_required
def view_inv(request):
    return render(request, 'myapp/data.html')

@login_required
def get_sheet(request):
    headers = {
        'api_key': settings.API_KEY
    }
    try:
        response = requests.get('http://ec2-18-188-29-216.us-east-2.compute.amazonaws.com:8000/api/visualizar_dados_investimentos', headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {'detail': 'Error fetching data', 'error': str(e)}
    return JsonResponse(data)

@login_required
def update_data(request):
    headers = {
        'api_key': settings.API_KEY
    }
    try:
        response = requests.post('http://ec2-18-188-29-216.us-east-2.compute.amazonaws.com:8000/api/atualizar_dados_investimentos', headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {'detail': 'Error updating data', 'error': str(e)}
    return JsonResponse(data)
