import requests
from django.http import JsonResponse

WEATHERBIT_API_KEY = '1d9546c0a8d644719d74176fec92b35a'

def current_weather(request):
    location = request.GET.get('location')
    if not location:
        return JsonResponse({'error': 'Location parameter is required.'}, status=400) #400 code, Location is not inputted.
    
    url = f'https://api.weatherbit.io/v2.0/current?city={location}&key={WEATHERBIT_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200: #200 code, success
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Unable to fetch current weather data.'}, status=500) #500 code, Server communication problems

def weather_forecast(request):
    location = request.GET.get('location')
    if not location:
        return JsonResponse({'error': 'Location parameter is required.'}, status=400)

    url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={location}&key={WEATHERBIT_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Unable to fetch weather forecast data.'}, status=500)

def weather_history(request):
    location = request.GET.get('location')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    if not location or not start_date or not end_date:
        return JsonResponse({'error': 'Location, start date, and end date parameters are required.'}, status=400)

    url = f'https://api.weatherbit.io/v2.0/history/daily?city={location}&start_date={start_date}&end_date={end_date}&key={WEATHERBIT_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Unable to fetch weather history data.'}, status=500)

