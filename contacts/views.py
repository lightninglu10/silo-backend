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
from .serializers import UserSerializer, ContactSerializer, GroupSerializer

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
    notes = forms.CharField(required=False)

class GroupsViewSet(viewsets.GenericViewSet):
    """
    View for groups
    """

    queryset = ()

    def list(self, request):
        """
        Grabs all of the user's groups
        """

        user = request.user
        all_groups = user.group.all()
        serialized_groups = GroupSerializer(all_groups, many=True)

        return Response({'groups': serialized_groups.data})

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

class ContactCardView(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    View to get specific contacts, modify contacts, and add contacts
    """

    serializer_class = ContactSerializer

    def retrieve(self, request, pk=None):
        try:
            contact = Contact.objects.get(number=pk)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact does not exist', 'status': 400})

        contact_serializer = ContactSerializer(contact)
        return Response({'contact': contact_serializer.data})

    def update(self, request, pk=None):
        """
        Edits the info of a specific contact
        """

        form = ContactForm(request.data)

        if form.is_valid():
            try:
                contact = Contact.objects.get(number=form.cleaned_data['number'])

                contact.email = form.cleaned_data['email']
                contact.first_name = form.cleaned_data['first_name']
                contact.last_name = form.cleaned_data['last_name']
                contact.notes = form.cleaned_data['notes']
                contact.saved = True
                contact.save()
            except Contact.DoesNotExist:
                if not request.user.is_authenticated():
                    return Response({'error': 'User is not authenticated', 'status': 403}, status=403)

                # TODO: Handle multiple contact books
                contact_book = request.user.contactBook.first()

                contact = Contact.objects.create(
                    contactBook=contact_book,
                    number=form.cleaned_data['number'],
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    notes=form.cleaned_data['notes'],
                    saved=True
                )
            contact_serializer = ContactSerializer(contact)
            return Response({'contact': contact_serializer.data, 'status': 200})

        return Response({'error': form.errors, 'status': 400}, status=200)
