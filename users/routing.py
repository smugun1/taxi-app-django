from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/ride-updates/<str:ride_id>/', consumers.RideUpdateConsumer.as_asgi()),
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
]