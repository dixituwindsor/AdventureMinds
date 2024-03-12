from django.urls import re_path

from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/chat/group/(?P<group_name>\w+)/$', consumer.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/private/(?P<username>\w+)/$', consumer.ChatConsumer.as_asgi()),
]









# from django.urls import path, include
# from mainapp.consumer import ChatConsumers
#
# websocket_url_patterns = [
#     path("", ChatConsumers.as_asgi()),
# ]