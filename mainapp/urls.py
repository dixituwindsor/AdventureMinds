from django.urls import path, include
from . import views

app_name = 'mainapp'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('myprofile/', views.user_profile, name='profile'),
    path('preferences/', views.user_preferences, name='user_preferences'),
    path('chat_app/', views.chat_app, name='chat_app'),
    path('add_trip/', views.add_trip, name='add_trip'),
    path('t/', views.terms_conditions, name='terms_conditions'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('trip_list/', views.trip_list, name='trip_list'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('getusers/', views.getusers, name='getusers'),
    path('forgotpassword/', views.forgot_password, name='forgotpassword')
]
