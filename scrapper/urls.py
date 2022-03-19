from django.urls import path
from . import views
app_name = 'scrapper'

urlpatterns = [
    path('get_weather/', views.home, name='weather_home'),
]