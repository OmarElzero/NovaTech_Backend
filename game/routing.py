from django.urls import re_path
from game.consumers import ExoplanetConsumer

websocket_urlpatterns = [
    re_path(r'ws/exoplanet/(?P<code>\w+)/$', ExoplanetConsumer.as_asgi()),
]
