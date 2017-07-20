# coding: utf-8

"""Forms to Propery"""

from django import forms
from django.contrib.auth.models import User

from .models import Property


class PropertyCreateForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title',
            'description',
            'address',
            'image',
            'is_available',
            'price',
            'property_type']
        labels = {'image': ''}


class PropertyDetailForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title',
            'description',
            'address',
            'image',
            'is_available',
            'price',
            'property_type']
        labels = {'image': ''}
