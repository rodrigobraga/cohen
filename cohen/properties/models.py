# coding: utf-8

"""Models to Property"""

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from django.contrib.gis.db.models import PointField

from .tasks import update_coordinates


PROPERTY_TYPE = (
    ('house', 'House'),
    ('apartment', 'Apartment/Flat'),
    ('townhouse', 'Townhouse'),
    ('commercial', 'Commercial/Industrial')
)


class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=255)
    point = PointField(null=True, blank=True, srid=4326)
    image = models.ImageField(upload_to='properties')
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    property_type = models.CharField(
        max_length=24, choices=PROPERTY_TYPE, default='house')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date', '-updated_date', 'title']
        verbose_name_plural = 'properties'

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('property-update', (), {'slug': self.slug})


@receiver(post_save, sender=Property)
def get_coordinates(sender, instance, **kwargs):
    update_coordinates.delay(instance.id, instance.address)
