from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import requests
from django.views import View


def get_weather(request):
    return render(request, 'automation/weather.html')


class GetWeather(View):
    def get(self, request):
        api_key = settings.WEATHER_API_KEY
        city = request.GET.get('city', None)
        base_url = 'https://api.openweathermap.org/data/2.5/weather'
        request_url = f'{base_url}?q={city}&appid={api_key}'
        response = requests.get(request_url)
        detail = {}
        if response.status_code == 200:
            data = response.json()
            description = data['weather'][0]['description']
            temperature = round(data['main']['temp'] - 273.15, 2)
            latitude = data['coord']['lat']
            longitude = data['coord']['lon']
            weather_type = data['weather'][0]['main']
            feels_like = round(data['main']['feels_like'] - 273.15, 2)
            min_temp = round(data['main']['temp_min'] - 273.15, 2)
            max_temp = round(data['main']['temp_max'] - 273.15, 2)
            pressure = data['main']['pressure']  # in hPa
            humidity = data['main']['humidity']  # in %
            visibility = data['visibility']  # in km

            detail['description'] = description
            detail['temperature'] = temperature
            detail['latitude'] = latitude
            detail['longitude'] = longitude
            detail['weather_type'] = weather_type
            detail['feels_like'] = feels_like
            detail['min_temp'] = min_temp
            detail['max_temp'] = max_temp
            detail['pressure'] = pressure
            detail['humidity'] = humidity
            detail['visibility'] = visibility
            return JsonResponse(detail)
        else:
            detail['description'] = 'Not Available'
            detail['temperature'] = 'Not Available'
            return JsonResponse(detail)