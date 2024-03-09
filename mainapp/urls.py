from django.urls import path
from . import views

app_name = 'mainapp'
urlpatterns = [
    # path('', views.messenger, name='messenger'),
    path('profile/', views.user_profile, name='profile'),
    path('preferences/', views.user_preferences, name='user_preferences'),
    path('chat_app/', views.chat_app, name='chat_app'),
    path('', views.messenger, name='messenger'),
    path('home/', views.messenger, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]