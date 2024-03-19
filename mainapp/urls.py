from django.urls import path, include
from . import views

app_name = 'mainapp'
urlpatterns = [
    path('chat_app/', views.chat_app, name='chat_app'),
    path('message_button/', views.message_button, name='message_button'),
    path('h/', views.homepage, name='homepage'),
    path('t/', views.terms_conditions, name='terms_conditions'),
    path('', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('getusers/', views.getusers, name='getusers'),
    path('accounts/', include('django.contrib.auth.urls')),
]
