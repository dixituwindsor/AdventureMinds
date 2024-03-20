from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('chat_app/', consumers.ChatConsumer.as_asgi()),
]