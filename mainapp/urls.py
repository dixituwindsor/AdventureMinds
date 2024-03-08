from django.urls import path
from . import views

app_name = 'mainapp'
urlpatterns = [
    # path('', views.messenger, name='messenger'),
    path('profile/', views.user_profile, name='profile'),
    path('preferences/', views.user_preferences, name='user_preferences'),
]