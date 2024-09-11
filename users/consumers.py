from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message = json.loads(text_data)
        notification_type = message.get('type')
        if notification_type == 'ride_status_update':
            # Process ride status update notification
            await self.send(text_data=json.dumps({
                'type': 'notification',
                'message': 'Your ride status has been updated.'
            }))

class RideUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['ride_id']
        self.room_group_name = f'ride_updates_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'ride_update_message',
                'message': message
            }
        )

    async def ride_update_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))