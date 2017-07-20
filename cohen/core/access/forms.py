# coding: utf-8

"""Forms to Access"""

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input'}))

    password = forms.CharField(
        label='Password',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input'}))
