import django
django.setup()
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Exoplanet, Users


User = get_user_model()

class ExoplanetConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the token from the URL parameters
        token = self.scope['query_string'].decode('utf-8').split('token=')[-1]
        exoplanet_code = self.scope['url_route']['kwargs']['code']

        user = await self.get_user_from_token(token)
        if not user:
            await self.close()
            return

        # Fetch the exoplanet by code
        exoplanet = await self.get_exoplanet_by_code(exoplanet_code)
        if not exoplanet:
            await self.close()  # Close connection if invalid exoplanet code
            return

        # Get user profile
        user_profile = await self.get_user_profile(user)

        # Check if the user has unlocked the exoplanet
        if await self.is_exoplanet_unlocked(user_profile, exoplanet.id):
            await self.accept()  # Accept the connection
        else:
            await self.close()  # Close if the user hasn't unlocked the exoplanet

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            # Fetch the token object
            token_obj = Token.objects.get(key=token)
            return token_obj.user  # Return the associated user
        except Token.DoesNotExist:
            return None  # Invalid token

    @database_sync_to_async
    def get_exoplanet_by_code(self, code):
        try:
            return Exoplanet.objects.get(code=code)
        except Exoplanet.DoesNotExist:
            return None  # Invalid exoplanet code

    @database_sync_to_async
    def get_user_profile(self, user):
        return Users.objects.get(user=user)

    @database_sync_to_async
    def is_exoplanet_unlocked(self, user_profile, exoplanet_id):
        return user_profile.unlocked_exoplanets.filter(id=exoplanet_id).exists()

    async def unlock_exoplanet(self, exoplanet_code):
        # Implement the unlock logic here
        pass
