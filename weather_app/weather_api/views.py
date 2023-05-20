import requests
from django.http import JsonResponse

WEATHERBIT_API_KEY = '1d9546c0a8d644719d74176fec92b35a'

def current_weather(request):
    location = request.GET.get('location')
    url = f'https://api.weatherbit.io/v2.0/current?city={location}&key={WEATHERBIT_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)

def weather_forecast(request):
    location = request.GET.get('location')
    url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={location}&key={WEATHERBIT_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)

def weather_history(request):
    location = request.GET.get('location')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    url = f'https://api.weatherbit.io/v2.0/history/daily?city={location}&start_date={start_date}&end_date={end_date}&key={WEATHERBIT_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)

