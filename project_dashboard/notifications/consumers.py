import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification
from django.contrib.auth.models import User



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user =self.scope['user']
        if self.user.is_authenticated:
            self.room_group_name=f'notifications_{self.user.id}'


            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )


            await self.accept()

        else:
            await self.close()


    async def disconnect(self, close_code):
        if hasattr(self,'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

        
    async def receive(self, text_data):
        text_data_json =json.loads(text_data)
        message=text_data_json['message']



        await self.channel_layer.group_send(
            self.room_group_name
            {
                'type':'notification_message',
                'message':message
            }
        )

    async def notification_message(self,event):
        message =event['message']


        await self.send(text_data=json.dumps({
            'message':message

        }))


@database_sync_to_async
def get_notifications(self):
    return(self.user.notification.filter(is_read=False).value(
        'id','message','created_at','related_task__title'

    ))
