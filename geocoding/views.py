from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import GeocodeSerializer  # Assuming you have this serializer defined


class GeocodeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GeocodeSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            mapbox_token = settings.MAPBOX_ACCESS_TOKEN  # Retrieve token from settings
            url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json?access_token={mapbox_token}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['features']:
                    coordinates = data['features'][0]['center']
                    return Response({'coordinates': coordinates}, status=status.HTTP_200_OK)
                return Response({'error': 'No results found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'error': 'Error connecting to Mapbox API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def geocode(request):
    serializer = GeocodeSerializer(data=request.data)
    if serializer.is_valid():
        query = serializer.validated_data['query']
        # Logic to interact with Mapbox or other geocoding services
        return Response({'coordinates': [0, 0]})  # Example response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
