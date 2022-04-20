from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.home, name='home'),
    path('enter_room/', views.enter_room, name='enter_room'),
    path('<str:room_name>/<str:username>/', views.room, name='room'),
    path('send/', views.SaveMessages.as_view(), name='save_messages'),
    path('get_room_messages/', views.GetMessages.as_view(), name='get_messages'),
    path('private_chat/', views.private_chat, name='private_chat'),
    path('private/<str:sender>/<str:receiver>/', views.private, name='private'),
    path('save_private/', views.SavePrivate.as_view(), name='save_private'),
    path('get_private_messages/', views.GetPrivate.as_view(), name='get_private_messages'),
]