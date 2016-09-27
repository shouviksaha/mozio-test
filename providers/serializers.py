import re
from rest_framework import serializers

from providers.models import Provider, ServiceArea


class ProviderSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    def validate_currency(self, value):
        if not len(value) == 3 and (value.isalpha() or value.isnumeric()):  # validating either 3-digit or 3-letter code
            raise serializers.ValidationError("Please enter proper currency values")
        return value

    # simple validation for phone as I'm not sure about the input format

    def validate_phone_number(self, value):
        # phone numbers shouldn't contain letters. Ignoring .ext. Minimum length of 8 include country code
        if re.search('[a-zA-Z]', value) or len(value) < 8:
            raise serializers.ValidationError("Please enter proper phone_number")

        return value

    class Meta:
        model = Provider
        fields = ('name', 'email', 'language', 'currency', 'phone_number', 'id')


class ServiceAreaSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    # conversion from GeoJSON to wkt and vice-versa handled by rest_framework_gis

    class Meta:
        model = ServiceArea
        fields = ('name', 'price', 'polygon', 'id')


class ServiceAreaQueryResponseSerializer(serializers.ModelSerializer):
    provider = serializers.ReadOnlyField(source='provider.name')

    class Meta:
        model = ServiceArea
        fields = ('name', 'price', 'provider')


class GenerateTokenQuerySerializer(serializers.Serializer):
    email = serializers.EmailField()
