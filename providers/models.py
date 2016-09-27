from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from rest_framework.authtoken.models import Token


class DateTimeMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Provider(User, DateTimeMixin):
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    currency = models.CharField(max_length=3)
    phone_number = models.CharField(max_length=15)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        create_token = False
        try:
            provider = Provider.objects.get(id=self.id)
        except Provider.DoesNotExist:
            create_token = True

        self.username = self.email  # setting username as email as username taken in api
        super(Provider, self).save(*args, **kwargs)
        if create_token:
            Token.objects.create(user=self)  # creating token for provider auth


class ServiceArea(DateTimeMixin):
    id = models.AutoField(primary_key=True)
    provider = models.ForeignKey('Provider', related_name="service_areas")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    polygon = models.PolygonField(geography=True)  # Polygon field with 3d measurements from GeoDjango

    def __unicode__(self):
        return self.name
