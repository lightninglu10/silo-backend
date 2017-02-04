from django.shortcuts import render
from django import forms

# Models
from .models import Message
from contacts.models import Contact
from django.contrib.auth.models import User

# DRF
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics

# Twilio
from twilio.rest import Client
from twilio.exceptions import TwilioRestException

# Serializers
from .serializers import UserListSerializer

account_sid = "AC416bdd1fded5fa067f76ecd4381632d5"
auth_token = "f15d3e7ae578b4ec75a15b5fa41e1b0f"
SILO_MESSAGING_ID = 'MGb015f9b8cea6900c64af4b2d5f7fb6bc'

client = Client(account_sid, auth_token)

class MessageForm(forms.Form):
    body = forms.CharField(max_length=1600, strip=True, required=False)
    media_url = forms.CharField(strip=True, required=False)
    number = forms.CharField(max_length=17, strip=True, required=True)
    contact_book = forms.IntegerField()


class MessagesView(viewsets.GenericViewSet):
    """
    View to send messages via twilio
    """

    serializer_class = UserListSerializer

    def create(self, request):
        """
        Creates a twilio message to send to recipient.
        """
        form = MessageForm(request.POST)

        if form.is_valid():
            # TODO: Get real users here not hard coded
            user = User.objects.get(username='patricklu')
            try:
                contact = Contact.objects.get(number=form.cleaned_data['number'], contactBook=user.contactBook.all()[form.cleaned_data['contact_book']])
            except Contact.DoesNotExist:
                contact = Contact.objects.create(number=form.cleaned_data['number'], contactBook=user.contactBook.all()[form.cleaned_data['contact_book']])

            if form.cleaned_data['media_url']:
                try:
                    response = client.messages.create(
                                    to=form.cleaned_data['number'],
                                    messaging_service_sid=SILO_MESSAGING_ID,
                                    body=form.cleaned_data['body'],
                                    media_url=form.cleaned_data['media_url'])
                # TODO: get the exceptions done properly
                except e:
                    return Response({'error': 'error'})
            else:
                try:
                    response = client.messages.create(
                                    to=form.cleaned_data['number'],
                                    messaging_service_sid=SILO_MESSAGING_ID,
                                    body=form.cleaned_data['body'])
                # TODO: get the exceptions done properly
                except TwilioRestException as e:
                    return Response({'error': 'error'})
            
            Message.objects.create(to=contact,
                sender=user,
                body=form.cleaned_data['body'],
                media_url=form.cleaned_data['media_url'],
                twilio_sid=response.sid)
            return Response({'success': 'Phone number sent!'})
        else:
            return Response({'error': form.errors.as_json()})

    def list(self, request):
        """
        Grabs a list of all the users & returns it with the last message sent.
        """
        user = User.objects.get(username='patricklu')
        contact_book = user.contactBook.all().first()
        userList = []
        for contact in contact_book.contacts.all():
            messages = contact.messages.all()
            if len(messages) > 0:
                userList.append(messages.last())

        userListData = UserListSerializer(userList, many=True).data
        return Response({'userList': userListData})
