from django.conf.urls.static import static
from django.urls import path, include
from AdventureMinds import settings
from . import views
from django.conf import settings


app_name = 'mainapp'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('myprofile/', views.user_profile, name='profile'),
    path('preferences/', views.user_preferences, name='user_preferences'),
    path('messages/', views.messages, name='messages'),
    path('message_button/', views.message_button, name='message_button'),
    path('create_group/', views.create_group, name='create_group'),
    path('', views.homepage, name='homepage'),
    path('homepage/', views.trip_list, name='trip_list'),
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
    path('add_rating/', views.add_rating, name='add_rating'),
    path('add_review/', views.add_review, name='add_review'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('getusers/', views.getusers, name='getusers'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mark_messages_as_read/', views.mark_messages_as_read, name='mark_messages_as_read'),
    path('set_last_active_userchat_id/', views.set_last_active_userchat_id, name='set_last_active_userchat_id'),
    path('contact_us/', views.contact_us, name='contact_us'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
