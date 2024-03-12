from django.urls import path
from . import views

app_name = 'mainapp'
urlpatterns = [
    path('chat_app/', views.chat_app, name='chat_app'),
    path('', views.messenger, name='messenger'),
    path('home/', views.messenger, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    # path('destination/<int:destination_id>/', views.destination_detail, name='destination_detail'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
]
