from django.urls import path
from weather_api import views

urlpatterns = [
    path('weather/current/', views.current_weather),
    path('weather/forecast/', views.weather_forecast),
    path('weather/history/', views.weather_history),
]