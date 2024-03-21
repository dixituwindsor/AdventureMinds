from django.urls import path
from . import views
from .views import PlaceDetailView

app_name = 'mainapp'
urlpatterns = [
    path('chat_app/', views.chat_app, name='chat_app'),
    path('', views.messenger, name='messenger'),
    path('home/', views.messenger, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('add_rating/<int:trip_id>/', views.add_rating, name='add_rating'),
    path('add_review/<int:trip_id>/', views.add_review, name='add_review'),
    path('place/<int:pk>/', PlaceDetailView.as_view(), name='place_detail'),
]
