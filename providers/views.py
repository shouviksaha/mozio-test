import json

from django.contrib.gis.geos import Point
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from providers.models import Provider, ServiceArea
from providers.serializers import ProviderSerializer, ServiceAreaSerializer, ServiceAreaQueryResponseSerializer
from providers.utils import InvalidArgumentsException


class ProviderListView(generics.ListCreateAPIView):
    """
    Endpoint for creating new providers and fetching providers list. \n
    Currency argument must be a 3-letter or a 3-digit code
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ProviderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint for updating provider and fetching provider details.
    Currency argument must be a 3-letter or a 3-digit code
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaListView(generics.ListCreateAPIView):
    """
    Endpoint for creating service areas and fetching service areas list.
    Polygon argument should be a valid GeoJSON of type polygon.
    Requires Authorization: Token <provider's token> header
    """
    serializer_class = ServiceAreaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return ServiceArea.objects.filter(provider=Provider.objects.get(user_ptr=self.request.user))

    def perform_create(self, serializer):
        serializer.save(provider=Provider.objects.get(user_ptr=self.request.user))


class ServiceAreaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        Endpoint for updating service area and fetching service area details.
        Polygon argument should be a valid GeoJSON of type polygon.
        Requires Authorization: Token <provider's token> header
    """
    def get_queryset(self):
        return ServiceArea.objects.filter(provider=Provider.objects.get(user_ptr=self.request.user))

    serializer_class = ServiceAreaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        serializer.save(provider=Provider.objects.get(user_ptr=self.request.user))


class ServiceAreaQueryView(APIView):
    """
        Endpoint for fetching service areas by lat/lng.
        Accepts "lat" and "lng" query params

    """
    def get(self, request, *args, **kwargs):
        params = request.query_params
        lat = params.get('lat', None)
        lng = params.get('lng', None)
        if lat and lng:
            try:
                lng = float(lng)
                lat = float(lat)
                pnt = Point(lng, lat)
            except (TypeError,ValueError):
                raise InvalidArgumentsException

            areas = ServiceArea.objects.filter(polygon__intersects=pnt)
            serializer = ServiceAreaQueryResponseSerializer(areas, many=True)
            return Response(serializer.data)
        else:
            raise InvalidArgumentsException
