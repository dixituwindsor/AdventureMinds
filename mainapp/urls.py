from django.urls import path
from . import views

app_name = 'mainapp'
urlpatterns = [
    path('', views.messenger, name='messenger'),
    path('profile/', views.userProfile, name='login')
]