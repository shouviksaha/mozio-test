from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import *


class CreateProviderTest(APITestCase):
    def setUp(self):
        self.data = {'name': 'Test Smith', 'email': 'test@test.com', 'language': 'test', 'currency': 'TST',
                     'phone_number': '+919739630033'}

    def test_can_create_provider(self):
        response = self.client.post('/api/providers/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadProviderTest(APITestCase):
    def setUp(self):
        self.data = {'name': 'Test Smith', 'email': 'test@test.com', 'language': 'test', 'currency': 'TST',
                     'phone_number': '+919739630033'}
        self.provider = Provider.objects.create(**self.data)

    def test_can_read_provider_list(self):
        response = self.client.get('/api/providers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_provider_detail(self):
        response = self.client.get('/api/providers/' + str(self.provider.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateProviderTest(APITestCase):
    def setUp(self):
        self.data = {'name': 'Test Smith', 'email': 'test@test.com', 'language': 'test', 'currency': 'TST',
                     'phone_number': '+919739630033'}
        self.provider = Provider.objects.create(**self.data)
        self.data.update({'language': 'new'})

    def test_can_update_user(self):
        response = self.client.put('/api/providers/' + str(self.provider.id), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Provider.objects.get(pk=self.provider.id).language, 'new')

    def test_can_partial_update_user(self):
        response = self.client.patch('/api/providers/' + str(self.provider.id), {'language': 'newer'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Provider.objects.get(pk=self.provider.id).language, 'newer')


class DeleteProviderTest(APITestCase):
    def setUp(self):
        self.data = {'name': 'Test Smith', 'email': 'test@test.com', 'language': 'test', 'currency': 'TST',
                     'phone_number': '+919739630033'}
        self.provider = Provider.objects.create(**self.data)

    def test_can_delete_user(self):
        response = self.client.delete('/api/providers/' + str(self.provider.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CreateServiceAreaTest(APITestCase):
    def setUp(self):
        self.provider_data = {'name': 'Test Smith', 'email': 'test@test.com', 'language': 'test', 'currency': 'TST',
                              'phone_number': '+919739630033'}

        self.provider = Provider.objects.create(**self.provider_data)
        self.area_data = {'name': 'Test area', 'price': '40.25',
                          'polygon': '{ "type": "Polygon", "coordinates": [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]]}'}

    def test_can_create_area(self):
        auth_token = self.provider.auth_token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token.key)
        response = self.client.post('/api/areas/', self.area_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadServiceAreaTest(APITestCase):
    def setUp(self):
        self.provider_data = {'name': 'Test Smith', 'email': 'test@test.com', 'language': 'test', 'currency': 'TST',
                              'phone_number': '+919739630033'}

        self.provider = Provider.objects.create(**self.provider_data)
        self.area_data = {'name': 'Test area', 'price': '40.25',
                          'polygon': '{ "type": "Polygon", "coordinates": [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]]}'}
        self.area = ServiceArea.objects.create(provider=self.provider, **self.area_data)

        self.new_provider_data = {'name': 'New Test Smith', 'email': 'newtest@test.com', 'language': 'test',
                                  'currency': 'TST',
                                  'phone_number': '+919739630033'}
        self.new_provider = Provider.objects.create(**self.new_provider_data)

    def test_can_read_area_list(self):
        auth_token = self.provider.auth_token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token.key)
        response = self.client.get('/api/areas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_area_detail(self):
        auth_token = self.provider.auth_token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token.key)
        response = self.client.get('/api/areas/' + str(self.area.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_read_others_area(self):
        auth_token = self.new_provider.auth_token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token.key)
        response = self.client.get('/api/areas/' + str(self.area.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateServiceAreaTest(APITestCase):
    def setUp(self):
        self.provider_data = {'name': 'Test Smith', 'email': 'test@test.com', 'language': 'test', 'currency': 'TST',
                              'phone_number': '+919739630033'}

        self.provider = Provider.objects.create(**self.provider_data)
        self.area_data = {'name': 'Test area', 'price': '40.25',
                          'polygon': '{ "type": "Polygon", "coordinates": [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]]}'}
        self.area = ServiceArea.objects.create(provider=self.provider, **self.area_data)

        self.area_data.update({'price': '50'})

    def test_can_update_area(self):
        auth_token = self.provider.auth_token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token.key)
        response = self.client.put('/api/areas/' + str(self.area.id), self.area_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ServiceArea.objects.get(pk=self.area.id).price, 50)

    def test_can_partial_update_area_detail(self):
        auth_token = self.provider.auth_token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token.key)
        response = self.client.patch('/api/areas/' + str(self.area.id), {'price': '60'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ServiceArea.objects.get(pk=self.area.id).price, 60)


class DeleteServiceAreaTest(APITestCase):
    def setUp(self):
        self.provider_data = {'name': 'Test Smith', 'email': 'test@test.com', 'language': 'test', 'currency': 'TST',
                              'phone_number': '+919739630033'}

        self.provider = Provider.objects.create(**self.provider_data)
        self.area_data = {'name': 'Test area', 'price': '40.25',
                          'polygon': '{ "type": "Polygon", "coordinates": [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]]}'}
        self.area = ServiceArea.objects.create(provider=self.provider, **self.area_data)

    def test_can_delete_service_area(self):
        auth_token = self.provider.auth_token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token.key)
        response = self.client.delete('/api/areas/' + str(self.area.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ServiceAreaQueryTest(APITestCase):
    def setUp(self):
        self.provider_data = {'name': 'Test Smith', 'email': 'test@test.com', 'language': 'test', 'currency': 'TST',
                              'phone_number': '+919739630033'}

        self.provider = Provider.objects.create(**self.provider_data)
        self.area_data = {'name': 'Test area', 'price': '40.25',
                          'polygon': '{ "type": "Polygon", "coordinates": [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]]}'}
        self.area = ServiceArea.objects.create(provider=self.provider, **self.area_data)

        self.correct_lat = 0.5
        self.correct_lng = 100.5
        self.incorrect_lat = 1.5

    def test_can_find_correct_query(self):
        response = self.client.get(
            '/api/get_areas/?lat={0}&lng={1}'.format(str(self.correct_lat), str(self.correct_lng)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_cannot_find_incorrect_query(self):
        response = self.client.get(
            '/api/get_areas/?lat={0}&lng={1}'.format(str(self.incorrect_lat), str(self.correct_lng)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
