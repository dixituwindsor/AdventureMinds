import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .models import Thread, ChatMessage, ChatGroup

User = get_user_model()


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        user = self.scope['user']
        if user.is_authenticated:
            self.user = user
            chat_room = f'user_chatroom_{user.id}'
            self.chat_room = chat_room
            await self.channel_layer.group_add(
                chat_room,
                self.channel_name
            )
            await self.send({
                'type': 'websocket.accept'
            })

    async def websocket_receive(self, event):
        received_data = json.loads(event['text'])
        message = received_data.get('message')
        thread_id = received_data.get('thread_id')
        user_id = received_data.get('sender_id')
        receiver_id = received_data.get('receiver_id')

        if not message or not thread_id or not user_id:
            print('Error:: Incomplete message data')
            return False

        sender = await self.get_user(user_id)
        if receiver_id:
            receiver = await self.get_user(receiver_id)
        else:
            receiver = None
        thread_obj = await self.get_thread(thread_id)
        if not sender:
            print('Error:: sent by user is incorrect')
        if not thread_obj:
            print('Error:: Thread id is incorrect')

        message_obj = await self.save_message(sender, message, thread_obj)

        is_group_chat = await self.thread_has_group(thread_obj)
        if not is_group_chat:
            other_user_chat_room = f'user_chatroom_{receiver_id}'
            self_user = self.scope['user']
            response = {
                'message': message,
                'sent_by': str(self_user.id),
                'thread_id': thread_id,
                'send_time': message_obj.timestamp.strftime("%d %a, %H:%M"),
                'username': message_obj.user.username
            }

            await self.channel_layer.group_send(
                other_user_chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(response)
                }
            )

            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(response)
                }
            )
        else:
            group_id = await self.get_group_id(thread_obj)
            members = await self.get_group_members(group_id)
            for user in members:
                user = await user
                other_user_chat_room = f'user_chatroom_{user.id}'
                self_user = self.scope['user']
                response = {
                    'message': message,
                    'sent_by': str(self_user.id),
                    'thread_id': thread_id,
                    'send_time': message_obj.timestamp.strftime('%d %a, %H:%M'),
                    'username': message_obj.user.username
                }
                if user != sender:
                    await self.channel_layer.group_send(
                        other_user_chat_room,
                        {
                            'type': 'chat_message',
                            'text': json.dumps(response)
                        }
                    )
                else:
                    await self.channel_layer.group_send(
                        self.chat_room,
                        {
                            'type': 'chat_message',
                            'text': json.dumps(response)
                        }
                    )

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name
        )

    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def send_group_message(self, user_id, message, thread):
        # Ensure this operation is performed asynchronously
        members = await self.get_group_members(thread.group.id)
        for member in members:
            if member.id != user_id:
                await self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({
                        'message': message,
                        'sent_by': user_id,
                        'thread_id': thread.id
                    })
                })

    @database_sync_to_async
    def get_thread(self, thread_id):
        return Thread.objects.filter(id=thread_id).first()

    @database_sync_to_async
    def thread_has_group(self, thread_obj):
        return thread_obj.group is not None

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.filter(id=user_id).first()

    @database_sync_to_async
    def save_message(self, user, message, thread):
        return ChatMessage.objects.create(user=user, thread=thread, message=message)

    @database_sync_to_async
    def get_group_members(self, group_id):
        group = ChatGroup.objects.filter(id=group_id).first()
        if group:
            members = group.members.all()
            users = [self.get_user(member.id) for member in members]
            return users
        return []

    @database_sync_to_async
    def get_group_id(self, thread_obj):
        return thread_obj.group.id
