from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from users.models import Ride

User = get_user_model()


class RideTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass123')
        self.client.login(email='testuser@example.com', password='testpass123')

    def test_create_ride(self):
        url = reverse('ride-list-create')
        data = {'pickup_location': 'Location A', 'dropoff_location': 'Location B'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_accept_ride(self):
        # Create a ride to accept
        ride = Ride.objects.create(pickup_location='Location A', dropoff_location='Location B', status='requested')
        url = reverse('ride-accept', kwargs={'ride_id': ride.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complete_ride(self):
        # Create a ride in progress to complete
        ride = Ride.objects.create(pickup_location='Location A', dropoff_location='Location B', status='in_progress')
        url = reverse('ride-complete', kwargs={'ride_id': ride.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
