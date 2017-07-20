# coding: utf-8

"""Tests to Property"""

import os
import json
import mock
from mock import call

from django.contrib.gis.geos import Point
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from core.access.factories import UserFactory

from properties.tasks import update_coordinates
from properties.factories import PropertyFactory


class PropertyCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        UserFactory(username='admin')

        self.client.login(username='admin', password='password')

    def test_get(self):
        response = self.client.get(reverse('property-add'))
        self.assertEqual(response.status_code, 200)

    @mock.patch('properties.models.update_coordinates')
    def test_post(self, m_coordinates):
        with open('/usr/src/app/core/static/logo.jpg', 'rb') as image:
            image.seek(0)
            response = self.client.post(
                reverse('property-add'),
                {
                    'title': 'The office',
                    'description': 'work',
                    'address': 'Rua do Carmo, 71 - Centro, Rio de Janeiro, RJ',
                    'image': SimpleUploadedFile('image.jpg', image.read()),
                    'is_available': True,
                    'price': 42.5,
                    'property_type': 'commercial'
                })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/property/the-office/')

        m_coordinates.delay.assert_called_once()

    def test_post_invalid_form(self):
        response = self.client.post(reverse('property-add'), {
            'title': 'a error',
            'property_type': 'home',
            'price': 7
        })

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', 'address', 'This field is required.')

    def test_post_login_required(self):
        self.client.logout()

        response = self.client.get(reverse('property-add'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/property/add/')


class PropertyListViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    @mock.patch('properties.models.update_coordinates')
    def test_get(self, m_coordinates):
        PropertyFactory.create_batch(3)

        PropertyFactory(title='not available', is_available=False)

        response = self.client.get(reverse('property-available'))
        self.assertEqual(response.status_code, 200)

        qs = response.context['object_list']

        self.assertEqual(qs.count(), 3)


class PropertyDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    @mock.patch('properties.models.update_coordinates')
    def test_get(self, m_coordinates):
        office = PropertyFactory(
            title='Point A',
            address='Rua do Carmo',
            point=Point(-22.902935, -43.176592))

        related = PropertyFactory(
            title='Point B',
            address='Rio Branco',
            point=Point(-22.907005, -43.176262))

        far = PropertyFactory(
            title='Point C',
            address='Parati',
            point=Point(-23.167065, -44.139270))

        response = self.client.get(
            reverse('property-available-detail', args=[office.slug]))
        self.assertEqual(response.status_code, 200)

        qs = response.context['related']

        self.assertEqual(qs.count(), 1)
        self.assertIsNotNone(qs.get(title=related.title))


class PropertyDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        UserFactory(username='admin')

        self.client.login(username='admin', password='password')

    @mock.patch('properties.models.update_coordinates')
    def test_get(self, m_coordinates):
        office = PropertyFactory()

        response = self.client.get(
            reverse('property-delete', args=[office.slug]))
        self.assertEqual(response.status_code, 200)

    @mock.patch('properties.models.update_coordinates')
    def test_delete(self, m_coordinates):
        office = PropertyFactory()

        response = self.client.delete(
            reverse('property-delete', args=[office.slug]))
        self.assertEqual(response.status_code, 302)


class PropertyUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        UserFactory(username='admin')

    @mock.patch('properties.models.update_coordinates')
    def test_post(self, m_coordinates):
        self.client.login(username='admin', password='password')

        office = PropertyFactory(
            address='Avenida Rio Branco, 156, Centro, Rio de Janeiro')

        response = self.client.post(
            reverse('property-update', args=[office.slug]),
            {
                'title': 'The Changed office',
                'description': 'work',
                'address': 'Rua do Carmo, 71 - Centro, Rio de Janeiro - RJ',
                'is_available': True,
                'price': 42.5,
                'property_type': 'commercial'
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/property/the-changed-office/')

        m_coordinates.delay.assert_called()

    @mock.patch('properties.models.update_coordinates')
    def test_post_invalid_form(self, m_coordinates):
        self.client.login(username='admin', password='password')

        office = PropertyFactory()

        response = self.client.post(
            reverse('property-update', args=[office.slug]),
            {
                'title': 'almost changed',
                'property_type': 'home',
                'price': 7
            })

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', 'address', 'This field is required.')


class PropertyListManagementViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        UserFactory(username='admin')

        self.client.login(username='admin', password='password')

    @mock.patch('properties.models.update_coordinates')
    def test_get(self, m_coordinates):
        PropertyFactory.create_batch(3)

        PropertyFactory(title='not available', is_available=False)

        response = self.client.get(reverse('property-list'))
        self.assertEqual(response.status_code, 200)

        qs = response.context['object_list']

        self.assertEqual(qs.count(), 4)


class UpdateCoordinatesTaskTest(TestCase):
    @mock.patch('properties.tasks.geocoder')
    def test_update_coordinates(self, m_geocoder):
        point = mock.Mock(lat=-22.902935, lng=-43.176592)
        m_geocoder.google.return_value = point

        # the task will be triggered by factory
        office = PropertyFactory(
            address='Lopes Mendes', point=Point(-23.167065, -44.139270))

        update_coordinates(office.id, office.address)

        m_geocoder.google.assert_called_once_with('Lopes Mendes')
