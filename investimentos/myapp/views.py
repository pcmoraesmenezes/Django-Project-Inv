from django.shortcuts import render
from django.http import JsonResponse
from .main import update_data_from_sheet, view_data_from_sheet

def home(request):
    return render(request, 'myapp/index.html')

def view_inv(request):
    return render(request, 'myapp/data.html')

def get_sheet(request):
    df = view_data_from_sheet()
    data = df.to_dict(orient='list')  # Converte o DataFrame para um dicionário
    return JsonResponse(data)

def update_data(request):
    selic, cdi, df = update_data_from_sheet()
    data = {
        'selic': selic,
        'cdi': cdi,
        'data_frame': df.to_dict(orient='list')  # Converte o DataFrame para um dicionário
    }
    return JsonResponse(data)
