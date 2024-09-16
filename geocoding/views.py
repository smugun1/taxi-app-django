from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import GeocodeSerializer  # Ensure you have this serializer defined
from rest_framework.permissions import AllowAny
import requests

class GeocodeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GeocodeSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            mapbox_token = settings.MAPBOX_ACCESS_TOKEN  # Retrieve token from settings
            url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json"
            params = {'access_token': mapbox_token}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['features']:
                    coordinates = data['features'][0]['center']
                    return Response({'longitude': coordinates[0], 'latitude': coordinates[1]}, status=status.HTTP_200_OK)
                return Response({'error': 'No results found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'error': 'Error connecting to Mapbox API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def geocode_view(request):
    location = request.data.get('query')
    if not location:
        return Response({"error": "Location not provided"}, status=status.HTTP_400_BAD_REQUEST)

    # Make a request to the Mapbox Geocoding API
    mapbox_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json"
    params = {
        'access_token': settings.MAPBOX_ACCESS_TOKEN,  # Use your Mapbox token
        'limit': 1  # Limit to 1 result
    }
    response = requests.get(mapbox_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if len(data['features']) > 0:
            coordinates = data['features'][0]['geometry']['coordinates']
            return Response({"longitude": coordinates[0], "latitude": coordinates[1]}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No results found for the given location"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "Error with geocoding service"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)