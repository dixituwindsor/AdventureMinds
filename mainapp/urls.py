from django.urls import path, include
from . import views

app_name = 'mainapp'
urlpatterns = [
    # path('', views.messenger, name='messenger'),
    path('profile/', views.user_profile, name='profile'),
    path('preferences/', views.user_preferences, name='user_preferences'),
    path('chat_app/', views.chat_app, name='chat_app'),
    path('add_trip/', views.add_trip, name='add_trip'),
    path('h/', views.homepage, name='homepage'),
    path('t/', views.terms_conditions, name='terms_conditions'),
    path('', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('getusers/', views.getusers, name='getusers'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add/', views.trip_add, name='trip_add'),
    path('added/', views.trip_added, name='trip_added'),
    path('place/add/', views.place_add, name='place_add'),
    path('interest/add/', views.interest_add, name='interest_add'),
    path('place/added/', views.place_added, name='place_added'),
    path('interest/added/', views.interest_added, name='interest_added'),
]