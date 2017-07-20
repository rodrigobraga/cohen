# coding: utf-8

"""Tests to Access"""

import json

from django.test import TestCase, Client
from django.urls import reverse

from core.access.factories import UserFactory


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        UserFactory(username='admin')

    def test_get(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'password'
        })

        self.assertEqual(302, response.status_code)
        self.assertEqual(response.url, '/property/')

    def test_post_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'foo',
            'password': 'bar'
        })

        self.assertEqual(response.status_code, 200)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('logout'))

        self.assertEqual(302, response.status_code)
        self.assertEqual(response.url, '/property/available/')
