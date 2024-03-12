from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        recipient_username = text_data_json.get('recipient_username')

        if recipient_username:
            # Private message
            recipient = await self.get_user_by_username(recipient_username)
            if recipient:
                await self.send_private_message(message, recipient)
        else:
            # Group message
            await self.send_group_message(message)

    async def send_private_message(self, message, recipient):
        await self.channel_layer.group_send(
            f'private_{recipient.username}',
            {
                'type': 'private_message',
                'message': message
            }
        )

    async def send_group_message(self, message):
        # Assuming you have a way to determine the group for the message
        group_name = 'your_group_name'
        await self.channel_layer.group_send(
            f'chat_{group_name}',
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def private_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def get_user_by_username(self, username):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            return await User.objects.get(username=username)
        except User.DoesNotExist:
            return None













# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
#
# class ChatConsumers(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = "group_chat_gfg"
#         await self.channel_layer.group_add(
#             self.room_name,
#             self.channel_name
#         )
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_name,
#             self.channel_layer
#         )
#
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         username = text_data_json["username"]
#         await self.channel_layer.group_send(
#             self.room_name,
#             {
#                 "type": "sendMessage",
#                 "message": message,
#                 "username": username,
#             }
#         )
#
#     async def sendMessage(self, event):
#         message = event["message"]
#         username = event["username"]
#         await self.send(text_data=json.dumps({"message": message, "username": username}))