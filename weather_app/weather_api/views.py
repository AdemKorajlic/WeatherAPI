import requests
import logging
from django.http import JsonResponse
from django.core.cache import cache
from datetime import datetime
from django.contrib.auth.decorators import login_required
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response



WEATHERBIT_API_KEY = '1d9546c0a8d644719d74176fec92b35a'
CACHE_EXPIRATION = 600  # Cache timeout 10 min

logging.basicConfig(filename='weather_api.log', level=logging.INFO)

def log_request(request):
    # Log request details
    logging.info(f'Request - Method: {request.method}, Path: {request.path}, Params: {request.GET.dict()}')

def log_response(response):
    # Log response details
    logging.info(f'Response - Status: {response.status_code}, Content: {response.content.decode()}')

@swagger_auto_schema(
    method='GET',
    operation_summary='Get current weather',
    operation_description='Get the current weather for a specific location.',
    manual_parameters=[
        openapi.Parameter(
            name='location',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Location for which to fetch weather information.',
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description='Current weather data retrieved successfully.',
            examples={
                'application/json': {
                    'temperature': 25,
                    'humidity': 60,
                    'wind_speed': 10,
                    'last_refresh': '2023-05-21T12:00:00Z'
                }
            }
        ),
        400: openapi.Response(
            description='Location parameter is required.',
            examples={
                'application/json': {
                    'error': 'Location parameter is required.'
                }
            }
        ),
        500: openapi.Response(
            description='Unable to fetch current weather data.',
            examples={
                'application/json': {
                    'error': 'Unable to fetch current weather data.'
                }
            }
        )
    }
)

@api_view(['GET'])
@login_required
def current_weather(request):
    location = request.GET.get('location')
    if not location:
        log_request(request)
        return JsonResponse({'error': 'Location parameter is required.'}, status=400)

    cache_key = f'current_weather_{location}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data)

    url = f'https://api.weatherbit.io/v2.0/current?city={location}&key={WEATHERBIT_API_KEY}'
    response = requests.get(url)
    log_request(request)
    log_response(response)

    if response.status_code == 200:
        data = response.json()

        # Add last refresh datetime to response
        data['last_refresh'] = cache.get(cache_key + '_refreshed')

        # Store data in cache
        cache.set(cache_key, data, CACHE_EXPIRATION)
        cache.set(cache_key + '_refreshed', datetime.now(), CACHE_EXPIRATION)

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Unable to fetch current weather data.'}, status=500)
    
@swagger_auto_schema(
    method='GET',
    operation_summary='Get weather forecast',
    operation_description='Get the weather forecast for a specific location.',
    manual_parameters=[
        openapi.Parameter(
            name='location',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Location for which to fetch weather forecast.',
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description='Weather forecast data retrieved successfully.',
            examples={
                'application/json': {
                    'forecast': [
                        {
                            'date': '2023-05-21',
                            'temperature': 25,
                            'humidity': 60,
                            'wind_speed': 10
                        },
                        {
                            'date': '2023-05-22',
                            'temperature': 28,
                            'humidity': 55,
                            'wind_speed': 12
                        }
                    ],
                    'last_refresh': '2023-05-21T12:00:00Z'
                }
            }
        ),
        400: openapi.Response(
            description='Location parameter is required.',
            examples={
                'application/json': {
                    'error': 'Location parameter is required.'
                }
            }
        ),
        500: openapi.Response(
            description='Unable to fetch weather forecast data.',
            examples={
                'application/json': {
                    'error': 'Unable to fetch weather forecast data.'
                }
            }
        )
    }
)

@api_view(['GET'])
@login_required
def weather_forecast(request):
    location = request.GET.get('location')
    if not location:
        log_request(request)
        return JsonResponse({'error': 'Location parameter is required.'}, status=400)

    cache_key = f'weather_forecast_{location}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data)

    url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={location}&key={WEATHERBIT_API_KEY}'
    response = requests.get(url)
    log_request(request)
    log_response(response)

    if response.status_code == 200:
        data = response.json()

        data['last_refresh'] = cache.get(cache_key + '_refreshed')

        cache.set(cache_key, data, CACHE_EXPIRATION)
        cache.set(cache_key + '_refreshed', datetime.now(), CACHE_EXPIRATION)

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Unable to fetch weather forecast data.'}, status=500)
    
@swagger_auto_schema(
    method='GET',
    operation_summary='Get weather history',
    operation_description='Get the weather history for a specific location and date range.',
    manual_parameters=[
        openapi.Parameter(
            name='location',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Location for which to fetch weather history.',
            required=True
        ),
        openapi.Parameter(
            name='start',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Start date of the weather history (YYYY-MM-DD).',
            required=True
        ),
        openapi.Parameter(
            name='end',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='End date of the weather history (YYYY-MM-DD).',
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description='Weather history data retrieved successfully.',
            examples={
                'application/json': {
                    'history': [
                        {
                            'date': '2023-05-19',
                            'temperature': 22,
                            'humidity': 65,
                            'wind_speed': 8
                        },
                        {
                            'date': '2023-05-20',
                            'temperature': 20,
                            'humidity': 70,
                            'wind_speed': 6
                        }
                    ],
                    'last_refresh': '2023-05-21T12:00:00Z'
                }
            }
        ),
        400: openapi.Response(
            description='Location, start date, and end date parameters are required.',
            examples={
                'application/json': {
                    'error': 'Location, start date, and end date parameters are required.'
                }
            }
        ),
        500: openapi.Response(
            description='Unable to fetch weather history data.',
            examples={
                'application/json': {
                    'error': 'Unable to fetch weather history data.'
                }
            }
        )
    }
)

@api_view(['GET'])
@login_required
def weather_history(request):
    location = request.GET.get('location')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    if not location or not start_date or not end_date:
        log_request(request)
        return JsonResponse({'error': 'Location, start date, and end date parameters are required.'}, status=400)

    cache_key = f'weather_history_{location}_{start_date}_{end_date}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data)

    url = f'https://api.weatherbit.io/v2.0/history/daily?city={location}&start_date={start_date}&end_date={end_date}&key={WEATHERBIT_API_KEY}'
    response = requests.get(url)
    log_request(request)
    log_response(response)

    if response.status_code == 200:
        data = response.json()

        data['last_refresh'] = cache.get(cache_key + '_refreshed')

        cache.set(cache_key, data, CACHE_EXPIRATION)
        cache.set(cache_key + '_refreshed', datetime.now(), CACHE_EXPIRATION)

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Unable to fetch weather history data.'}, status=500)