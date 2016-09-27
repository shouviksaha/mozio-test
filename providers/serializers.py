from rest_framework import serializers

from providers.models import Provider, ServiceArea


class ProviderSerializer(serializers.ModelSerializer):
    auth_token = serializers.ReadOnlyField(source='auth_token.key')
    id = serializers.ReadOnlyField()

    def validate_currency(self,value):
        if not len(value) == 3 and (value.isalpha() or value.isnumeric()):
            raise serializers.ValidationError("Please enter proper currency values")
        return value


    class Meta:
        model = Provider
        fields = ('name', 'email', 'language', 'currency', 'phone_number', 'auth_token', 'id')


class ServiceAreaSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = ServiceArea
        fields = ('name', 'price', 'polygon', 'id')


class ServiceAreaQueryResponseSerializer(serializers.ModelSerializer):
    provider = serializers.ReadOnlyField(source='provider.name')

    class Meta:
        model = ServiceArea
        fields = ('name', 'price', 'provider')
