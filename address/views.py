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

    def get_object_instance(self, input):
        return Address.objects.filter(address__icontains=input)

    def get_instance(self, input):
        # check database if address from/to exist
        # if exists, return lat and lng
        try:
            return self.get_object_instance(input)[:1].get()
        except Address.DoesNotExist:
            # if not, use Google API to get lat and lng and insert into DB and return lat and lng
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address=${input.replace(' ', '+')}+USA&key={settings.API_KEY}"
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()
                # get the first result
                result = data.get("results", [])[0]
                # if exist, the store the data into db for faster retrieval
                if result:
                    location = result["geometry"]["location"]
                    instance = Address.objects.create(
                        address=f"{input} ({result['formatted_address']})",
                        lng=location["lng"],
                        lat=location["lat"],
                    )
                    return instance
        # if the data is not found in db or Google Map API, then return None
        return None

    # I wrote this function based on the Haversine formula from this website: https://www.movable-type.co.uk/scripts/latlong.html
    def haversine(self, start_lat, start_lng, end_lat, end_lng):
        lat1 = radians(start_lat)
        lng1 = radians(start_lng)
        lat2 = radians(end_lat)
        lng2 = radians(end_lng)

        # Haversine formula
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 3958.7559  # 6371 km = 3958.7559 miles
        return c * r

    def create(self, request):
        serializer = DistanceSerializer(data=request.data)
        if serializer.is_valid():
            start = serializer.data.get("start", "")
            end = serializer.data.get("end", "")
            # start instance
            start_instance = self.get_instance(start)
            # end instance
            end_instance = self.get_instance(end)
            # init lat and lng of start and end to the equator
            start_lat = 0
            start_lng = 0
            end_lat = 0
            end_lng = 0
            # set start lat and lng if exist
            if start_instance:
                start_lat = start_instance.lat
                start_lng = start_instance.lng
            # set end lat and lng if exist
            if end_instance:
                end_lat = end_instance.lat
                end_lng = end_instance.lng
            # calculate distance
            distance = self.haversine(start_lat, start_lng, end_lat, end_lng)
            return Response(
                {
                    "start": start_instance.address,
                    "end": end_instance.address,
                    "distance": f"{round(distance, 2)} miles",
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
