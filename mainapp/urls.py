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
    # path('destination/<int:destination_id>/', views.destination_detail, name='destination_detail'),
    # path('trip/<int:trip_id>/add_review/', views.add_review, name='add_review'),
    # path('add_rating//', views.add_trip, name='add_trip'),
    path('add_review/<int:place_id>/', views.add_rating, name='add_rating'),
    # path('add_trip/', views.add_trip, name='add_trip'),
    path('add_review/<int:place_id>/', views.add_review, name='add_review'),
    # path('trip_info/<int:id>/', views.trip_info, name='trip_info'),
    # path('add_review/<int:id>/', views.add_review, name='add_review'),
    path('place/<int:pk>/', PlaceDetailView.as_view(), name='place_detail'),
]
