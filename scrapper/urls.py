from django.urls import path
from . import views
app_name = 'scrapper'

urlpatterns = [
    path('get_weather/', views.home, name='weather_home'),
    path('movie_home/', views.movie_home, name='movie_home'),
    path('weather_app/', views.weather_app, name='weather_app'),
    path('news/', views.naija_news, name='news'),
]