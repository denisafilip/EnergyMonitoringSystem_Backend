import json
from channels.generic.websocket import AsyncConsumer, WebsocketConsumer, AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected!!!!")
        self.client_id = self.scope["url_route"]["kwargs"]["client_id"]
        self.client_group = f"client_{self.client_id}"

        await self.channel_layer.group_add(self.client_group, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.client_group, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        notification = text_data_json["notification"]
        print(notification)

        await self.channel_layer.group_send(
            self.client_group, {"type": "notification", "notification": notification}
        )

    async def notification(self, event):
        notification = event["notification"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"notification": notification}))
