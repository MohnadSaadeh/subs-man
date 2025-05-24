import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
# from apps.home.models import Member



class SearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()  # Accept the WebSocket connection

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        from apps.home.models import Member  # Import inside the function

        data = json.loads(text_data)
        query = data.get('query', '')
        # Search members whose names start with the query
        # Run database query asynchronously
        members = await self.get_members(query)
        await self.send(text_data=json.dumps({'results': members }))

    @staticmethod
    @sync_to_async
    def get_members(query):
        from apps.home.models import Member  # Import inside the function
        # Fetch both ID and Name
        return list(Member.objects.filter(name__icontains=query).values('id','name'))