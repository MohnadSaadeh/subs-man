# routing.py  it like urls.py
# from django.urls import re_path
from django.urls import path
# from . import consumers
from .consumers import SearchConsumer

# websocket_urlpatterns = [
#     re_path(r'ws/search/$', consumers.SearchConsumer.as_asgi()),
# ]

websocket_urlpatterns = [
    path(r'ws/search/', SearchConsumer.as_asgi()), # 'ws/search/'
]