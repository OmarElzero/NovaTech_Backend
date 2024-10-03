
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NovaTech.settings')
import django
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from game.routing import websocket_urlpatterns

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NovaTech.settings')

# Ensure Django apps are loaded
# django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
