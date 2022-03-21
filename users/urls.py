from django.urls import path
from . import views, ajax_views

app_name = 'users'

urlpatterns = [
    path('home/', views.home, name='home'),
    #path('add_country/', views.add_country, name='add_country'),
    #path('add_city/', views.add_city, name='add_city'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),  # <-- this one here
    path('add_profile/', views.profile_create_view, name='add_profile'),
    path('profile_details/<int:id>', views.profile_details, name='profile_details'),
    path('user_profile/<int:id>/', views.user_profile, name='user_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('register_user/', views.signup_view, name='register_user'),
    path('login_user/', views.user_login, name='user_login'),
    path('logout_user/', views.user_logout, name='logout'),
    path('contact_me/', views.contact_me, name='contact_me'),
    path('add_project/', views.add_project, name='add_project'),
    path('project_details/<int:id>/<str:slug>/', views.project_details, name='project_details'),
    path('get_city_by_country/', ajax_views.get_city_by_country, name='get_city_by_country'),
    path('display_profile/', views.display_profile, name='display_profile'),
    path('owner_profile/', views.owner_profile, name='owner_profile'),
    path('load_more_project/', views.load_more_project, name='load_more_project'),
]