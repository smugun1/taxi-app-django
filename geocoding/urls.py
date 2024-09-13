from django.urls import path
from .views import GeocodeView

urlpatterns = [
    path('geocode/', GeocodeView.as_view(), name='geocode'),
]
