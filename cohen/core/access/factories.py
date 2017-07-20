# coding: utf-8

"""Factories to Access"""

from factory import DjangoModelFactory, Sequence, PostGenerationMethodCall

from django.contrib.auth.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = Sequence(lambda x: u'user %d' % x)
    is_superuser = True
    password = PostGenerationMethodCall('set_password', 'password')
