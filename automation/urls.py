from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('get_weather/', views.get_weather, name='get_weather'),
    path('weather_details/', views.GetWeather.as_view(), name='weather_details'),
]