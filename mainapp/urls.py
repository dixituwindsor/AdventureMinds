from django.urls import path
from . import views

app_name = 'mainapp'
urlpatterns = [
    path('', views.messenger, name='messenger'),
    path('h/', views.homepage, name='homepage'),
]