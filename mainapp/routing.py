from django.urls import path, include
from mainapp.consumer import ChatConsumers

websocket_url_patterns = [
    path("", ChatConsumers.as_asgi()),
]