from django.shortcuts import render
from django.dispatch import receiver

from allauth.account.signals import user_signed_up
from contacts.models import UserProfile, ContactBook

# DRF
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics

from django.contrib.auth import authenticate, login, logout
from django import forms

import random

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    # After a user signs up, create a user profile:

    UserProfile.objects.create(user=user, number=str(random.randrange(0, 99999999999999999)))
    ContactBook.objects.create(user=user)

class LoginForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)

class GetUserInfoView(viewsets.GenericViewSet):
    """
    View to get user info after login
    """

    def list(self, request):
        """
        Sends back user info
        """

        if request.user.is_authenticated():
            user = request.user
            return Response({'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'status': 200})
        else:
            return Response({'error': 'User is not authenticated', 'status': 403})
