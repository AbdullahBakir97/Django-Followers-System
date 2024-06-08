import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, ChatMessage
from accounts.models import User, OnlineUser

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_user(self, userId):
        return User.objects.get(id=userId)

    @database_sync_to_async
    def get_online_users(self):
        online_users = OnlineUser.objects.all()
        return [online_user.user.id for online_user in online_users]

    @database_sync_to_async
    def add_online_user(self, user):
        try:
            OnlineUser.objects.create(user=user)
        except:
            pass

    @database_sync_to_async
    def delete_online_user(self, user):
        try:
            OnlineUser.objects.get(user=user).delete()
        except:
            pass

    @database_sync_to_async
    def save_message(self, message, userId, roomId):
        user_obj = User.objects.get(id=userId)
        chat_obj = ChatRoom.objects.get(roomId=roomId)
        chat_message_obj = ChatMessage.objects.create(chat=chat_obj, user=user_obj, message=message)
        return {
            'action': 'message',
            'user': userId,
            'roomId': roomId,
            'message': message,
            'userImage': user_obj.profile.image.url,
            'userName': user_obj.first_name + " " + user_obj.last_name,
            'timestamp': str(chat_message_obj.timestamp)
        }

    async def send_online_user_list(self):
        online_user_list = await self.get_online_users()
        chat_message = {
            'type': 'chat_message',
            'message': {
                'action': 'onlineUser',
                'userList': online_user_list
            }
        }
        await self.channel_layer.group_send('onlineUser', chat_message)

    async def connect(self):
        self.userId = self.scope['url_route']['kwargs']['userId']
        self.userRooms = await database_sync_to_async(list)(ChatRoom.objects.filter(member=self.userId))
        for room in self.userRooms:
            await self.channel_layer.group_add(room.roomId, self.channel_name)
        await self.channel_layer.group_add('onlineUser', self.channel_name)
        self.user = await self.get_user(self.userId)
        await self.add_online_user(self.user)
        await self.send_online_user_list()
        await self.accept()

    async def disconnect(self, close_code):
        await self.delete_online_user(self.user)
        await self.send_online_user_list()
        for room in self.userRooms:
            await self.channel_layer.group_discard(room.roomId, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        roomId = text_data_json['roomId']
        chat_message = {}
        if action == 'message':
            message = text_data_json['message']
            userId = text_data_json['user']
            chat_message = await self.save_message(message, userId, roomId)
        elif action == 'typing':
            chat_message = text_data_json
        await self.channel_layer.group_send(roomId, {
            'type': 'chat_message',
            'message': chat_message
        })

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))