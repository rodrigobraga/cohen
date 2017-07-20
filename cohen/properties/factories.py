# coding: utf-8

"""Factories to Property"""

from factory import DjangoModelFactory, Sequence, SubFactory, LazyAttribute
from factory.django import ImageField

from django.utils.text import slugify

from core.access.factories import UserFactory
from .models import Property


class PropertyFactory(DjangoModelFactory):
    class Meta:
        model = Property

    title = Sequence(lambda x: u'title %d' % x)
    description = Sequence(lambda x: u'description %d' % x)
    slug = LazyAttribute(lambda a: slugify(a.title))
    address = Sequence(lambda x: u'address %d' % x)
    image = ImageField(color='blue')
    is_available = True
    price = 7
    created_by = SubFactory(UserFactory)
