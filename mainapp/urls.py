from django.urls import path
from . import views

app_name = 'mainapp'
urlpatterns = [
    path('chat_app/', views.chat_app, name='chat_app'),
]
