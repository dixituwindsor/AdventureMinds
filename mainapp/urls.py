from django.urls import path, include
from . import views


app_name = 'mainapp'
urlpatterns = [
    # path('', views.messenger, name='messenger'),
    path('myprofile/', views.user_profile, name='profile'),
    path('preferences/', views.user_preferences, name='user_preferences'),
    path('chat_app/', views.chat_app, name='chat_app'),
    path('add_trip/', views.add_trip, name='add_trip'),
    path('h/', views.homepage, name='homepage'),
    path('t/', views.terms_conditions, name='terms_conditions'),
    path('login/', views.user_login, name='login'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('trip_list/', views.trip_list, name='trip_list'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('getusers/', views.getusers, name='getusers'),
    path('accounts/', include('django.contrib.auth.urls')),
]
