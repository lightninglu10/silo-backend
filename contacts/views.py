from django.shortcuts import render
from django.dispatch import receiver

from allauth.account.signals import user_signed_up
from contacts.models import UserProfile, ContactBook, Contact

# DRF
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics

from django.contrib.auth import authenticate, login, logout
from django import forms

# Serializers
from .serializers import UserSerializer

import random

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    # After a user signs up, create a user profile:

    UserProfile.objects.create(user=user, number=str(random.randrange(0, 99999999999999999)))
    ContactBook.objects.create(user=user)

class ContactForm(forms.Form):
    email = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    number = forms.CharField(required=True)

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
            user_serialized = UserSerializer(user)
            return Response(user_serialized.data)
        else:
            return Response({'error': 'User is not authenticated', 'status': 403})

class ContactCardView(viewsets.GenericViewSet):
    """
    View to get specific contacts, modify contacts, and add contacts
    """

    def update(self, request, pk=None):
        """
        Edits the info of a specific contact
        """

        form = ContactForm(request.data)

        if form.is_valid():
            contact = Contact.objects.get(number=form.cleaned_data['number'])
            contact.email = form.cleaned_data['email']
            contact.first_name = form.cleaned_data['first_name']
            contact.last_name = form.cleaned_data['last_name']
            contact.save()
            return Response({'success': 'Contact updated', 'status': 200})

        return Response({'error': form.errors}, status=200)
