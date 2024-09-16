from rest_framework import serializers

class GeocodeSerializer(serializers.Serializer):
    query = serializers.CharField(required=True)
