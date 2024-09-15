from rest_framework import serializers

class GeocodeSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255)
