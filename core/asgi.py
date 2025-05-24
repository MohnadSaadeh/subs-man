# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter # new line WS
# from channels.auth import AuthMiddlewareStack 
from apps.home.routing import websocket_urlpatterns # new line WS # Import from apps.home.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()  # Ensure apps are loaded before importing anything

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # "websocket": URLRouter(home.routing.websocket_urlpatterns) # new line WS
    "websocket": URLRouter(websocket_urlpatterns)
})


