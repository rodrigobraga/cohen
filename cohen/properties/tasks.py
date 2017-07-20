# coding: utf-8

from celery import shared_task

import geocoder

from django.contrib.gis.geos import Point

@shared_task
def update_coordinates(id, address):
    from .models import Property

    g = geocoder.google(address)
    Property.objects.filter(pk=id).update(point=Point(g.lat, g.lng))
