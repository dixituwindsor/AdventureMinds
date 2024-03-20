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
    path('h/', views.trip_list, name='homepage'),
    path('add_trip/', views.add_trip, name='add_trip'),
    path('t/', views.terms_conditions, name='terms_conditions'),
    path('login/', views.user_login, name='login'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('trip_list/', views.trip_list, name='trip_list'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('join_trip/<int:trip_id>', views.join_trip, name='join_trip'),
    path('trip/<int:trip_id>/join-request/<int:request_id>/accept/', views.accept_join_request, name='accept_join_request'),
    path('trip/<int:trip_id>/join-request/<int:request_id>/decline/', views.decline_join_request,
         name='decline_join_request'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('getusers/', views.getusers, name='getusers'),
    path('accounts/', include('django.contrib.auth.urls')),
]
