from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/client/(?P<client_id>\d+)/$", consumers.NotificationConsumer.as_asgi()),
    # re_path(r"ws/client/", consumers.NotificationConsumer.as_asgi()),
]