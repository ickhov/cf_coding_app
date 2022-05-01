from django.urls import include, path
from rest_framework import routers
from address.views import DistanceViewSet

router = routers.SimpleRouter()
router.register(r"distance", DistanceViewSet, basename="distance")

urlpatterns = [
  path("", include(router.urls)),
]
