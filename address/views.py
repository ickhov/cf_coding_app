from math import asin, cos, radians, sin, sqrt
import requests
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.response import Response
from address.models import Address
from address.serializers import DistanceSerializer


class DistanceViewSet(viewsets.ViewSet):
    """
    A ViewSet for calculating the distance between 2 addresses.
    """

    def create(self, request):
        serializer = DistanceSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
