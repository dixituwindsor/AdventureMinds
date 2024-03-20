from django.urls import path, include
from . import views


app_name = 'mainapp'
urlpatterns = [
    # path('', views.messenger, name='messenger'),
    path('myprofile/', views.user_profile, name='profile'),
    path('preferences/', views.user_preferences, name='user_preferences'),
    path('messages/', views.messages, name='messages'),
    path('message_button/', views.message_button, name='message_button'),
    path('create_group/', views.create_group, name='create_group'),
    path('', views.homepage, name='homepage'),
    path('t/', views.terms_conditions, name='terms_conditions'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('getusers/', views.getusers, name='getusers'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mark_messages_as_read/', views.mark_messages_as_read, name='mark_messages_as_read'),
]
