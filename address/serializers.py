from rest_framework import serializers

class DistanceSerializer(serializers.Serializer):
  start = serializers.CharField()
  end = serializers.CharField()