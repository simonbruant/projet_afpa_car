import asyncio
import json

from django.contrib.auth import get_user_model
from django.utils import timezone

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage

class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected", event)

        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        print(other_user, me)
        thread_obj = await self.get_thread(me, other_user)
        print(me, thread_obj)
        self.thread_obj = thread_obj
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("receive", event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username

            my_reponse = {
                'message': msg,
                'username': username
            }
            await self.create_chat_message(user, msg)

            #broadcast the message
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(my_reponse)
                }
            )
    
    async def chat_message(self, event):
        #send the actual message
        print('message', event)
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

        
    async def websocket_disconnect(self, event):
        #when the socket connects
        print("disconnect", event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_chat_message(self, user, msg):
        thread_obj = self.thread_obj
        thread_obj.updated = timezone.now
        thread_obj.save()
        return ChatMessage.objects.create(thread=thread_obj, user=user, message=msg)