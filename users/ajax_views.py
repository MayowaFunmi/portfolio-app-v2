from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Country, City


def get_city_by_country(request):
    selected_country_id = request.GET.get('selected_country_id')
    selected_country = Country.objects.get(id=selected_country_id)
    cities = City.objects.filter(country=selected_country).order_by('name')
    t = render_to_string('users/city_by_country.html', {'data': cities})
    return JsonResponse({'data': t})