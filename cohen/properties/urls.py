# coding: utf-8

"""URL's to Access"""

from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .models import Property

from .views import (
    PropertyList,
    PropertyCreate,
    PropertyDetail,
    PropertyUpdate,
    PropertyDelete)

urlpatterns = [
    # add properties
    url(
        r'add/$',
        login_required(PropertyCreate.as_view()),
        name='property-add'),

    # list (available)
    url(
        r'available/$',
        PropertyList.as_view(
            template_name='properties/property_list_available.html',
            queryset=Property.objects.filter(is_available=True)),
        name='property-available'),
    url(
        r'available/(?P<slug>[\w-]+)/$',
        PropertyDetail.as_view(
            queryset=Property.objects.filter(is_available=True)),
        name='property-available-detail'),

    # delete
    url(
        r'(?P<slug>[\w-]+)/delete/$',
        login_required(PropertyDelete.as_view()),
        name='property-delete'),

    # update
    url(
        r'(?P<slug>[\w-]+)/$',
        login_required(PropertyUpdate.as_view()),
        name='property-update'),

    # list (administration)
    url(
        r'^$',
        login_required(PropertyList.as_view()),
        name='property-list'),
]
