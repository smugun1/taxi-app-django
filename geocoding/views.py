import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GeocodeSerializer

class GeocodeView(APIView):
    def post(self, request):
        serializer = GeocodeSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            mapbox_token = 'YOUR_MAPBOX_API_KEY'
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
