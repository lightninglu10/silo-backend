from django.shortcuts import render
from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django.views.decorators.csrf import csrf_exempt

# Models
from .models import Message
from contacts.models import Contact, UserProfile
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
from .serializers import UserListSerializer, MessagesSerializer

# Channels for websockets
from channels import Group

# Utils
import phonenumbers
import json
from operator import itemgetter

# Settings
from silo.settings import TWILIO_STATUS_CALLBACK

account_sid = "AC416bdd1fded5fa067f76ecd4381632d5"
auth_token = "f15d3e7ae578b4ec75a15b5fa41e1b0f"
SILO_MESSAGING_ID = 'MGb015f9b8cea6900c64af4b2d5f7fb6bc'
USA_NUMBER_LENGTH = 10

client = Client(account_sid, auth_token)

class OptInForm(forms.Form):
    number = forms.CharField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    country = forms.CharField(required=False)
    contact_book = forms.IntegerField()

class MessageForm(forms.Form):
    body = forms.CharField(max_length=1600, strip=True, required=False)
    media_url = forms.CharField(strip=True, required=False)
    numbers = SimpleArrayField(forms.CharField(strip=True), required=True)
    contact_book = forms.IntegerField()

class ReceiveMessageForm(forms.Form):
    Body = forms.CharField(strip=True, required=False)
    SmsSid = forms.CharField(strip=True, required=False)
    ToCountry = forms.CharField(strip=True, required=False)
    ToCity = forms.CharField(strip=True, required=False)
    NumSegments = forms.CharField(strip=True, required=False)
    MessagingServiceSid = forms.CharField(strip=True, required=False)
    NumMedia = forms.CharField(strip=True, required=False)
    From = forms.CharField(strip=True, required=False)
    FromZip = forms.CharField(strip=True, required=False)
    ToState = forms.CharField(strip=True, required=False)
    To = forms.CharField(strip=True, required=False)
    MessageStatus = forms.CharField(required=False)
    SmsStatus = forms.CharField(required=False)
    MessageSid = forms.CharField(required=False)

class OptInView(viewsets.GenericViewSet):
    """
    View to handle initial opt in's
    """

    permission_classes = ()

    def create(self, request):
        """
        Callback / post after opting into the text list
        """

        form = OptInForm(request.data)
        user = request.user
        if form.is_valid():
            number = form.cleaned_data['number']
            country_code = form.cleaned_data['country']
            parsed_number = phonenumbers.parse(number, country_code)
            E164 = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

            # Contact shouldn't exist
            try:
                contact = Contact.objects.create(number=E164,
                    contactBook=user.contactBook.all()[form.cleaned_data['contact_book']])
            except:
                return Response({'error': 'The number already exists!', 'status': 400})

            try:
                # TODO: make the status callback an environment variable
                response = client.messages.create(
                                to=number,
                                status_callback=TWILIO_STATUS_CALLBACK,
                                messaging_service_sid=SILO_MESSAGING_ID,
                                body=user.profile.opt_in_message)
            except TwilioRestException as e:
                # TODO: get the exceptions done properly
                return Response({'error': 'Twilio error', 'status': 400}, status=400)

            # TODO: get response.sid correct
            new_message = Message.objects.create(
                to=contact,
                sender=user,
                body=user.profile.opt_in_message,
                twilio_sid=response.sid,
            )

            new_message_serialized = MessagesSerializer(new_message)

            return Response({'success': 'Message sent!', 'message': new_message_serialized.data, 'status': 200})
        
        return Response({'error': form.errors.as_json(), 'status': 400}, status=400)

class MessagesViewStatus(viewsets.GenericViewSet):
    """
    View to check the status of messages: sent, failed, undelivered?
    """

    permission_classes = ()

    def create(self, request):
        """
        Callback for delivery status of a message
        """
        form = ReceiveMessageForm(request.data)

        if form.is_valid():
            try:
                message = Message.objects.get(twilio_sid=form.cleaned_data['MessageSid'])
            except Message.DoesNotExist:
                return Response({'error': 'The message does not exist', 'status': 400}, status=400)

        message.status(form.cleaned_data['MessageStatus'])
        return Response({'success': 'Message status kept', 'status': 200}, status=200)

class ReceiveMessagesView(viewsets.GenericViewSet):
    """
    View to receive messages via twilio
    """

    permission_classes = ()

    def create(self, request):
        """
        Webhook for receiving a message from twilio
        """

        form = ReceiveMessageForm(request.data)

        if form.is_valid():
            try:
                user = UserProfile.objects.get(number=form.cleaned_data['To']).user
            except UserProfile.DoesNotExist:
                return Response({'error': 'Phone number does not match with anyone', 'status': 400}, status=400)

            try:
                # TODO: Handle contact book correctly
                contact = Contact.objects.get(
                    number=form.cleaned_data['From'],
                    contactBook=user.contactBook.all()[0]
                )
            except Contact.DoesNotExist:
                contact = Contact.objects.create(
                    number=form.cleaned_data['From'],
                    contactBook=user.contactBook.all()[0]
                )

            new_message = Message.objects.create(
                body=form.cleaned_data['Body'],
                to=contact,
                media_url='',
                sender=user,
                twilio_sid=form.cleaned_data['SmsSid'],
                me=False
            )

            new_message_serialized = MessagesSerializer(new_message)

            Group('messages').send({'text': json.dumps(new_message_serialized.data)})

            return Response({'success': 'Message received'})

        return Response({'error': form.errors}, status=400)


class MessagesView(viewsets.GenericViewSet):
    """
    View to send messages via twilio
    """

    serializer_class = UserListSerializer
    permission_classes = ()

    def create(self, request):
        """
        Creates a twilio message to send to recipient.
        """
        form = MessageForm(request.data)

        if form.is_valid():

            if request.user.is_authenticated():
                user = request.user
            else:
                return Response({'error': 'User not logged in'}, status=403)

            contacts = []
            twilio_responses = []
            # TODO: Finish doing multi numbers
            for number in form.cleaned_data['numbers']:
                true_number = number
                if len(number) == USA_NUMBER_LENGTH:
                    true_number = "+1" + number
                try:
                    contact = Contact.objects.get(number=true_number,
                        contactBook=user.contactBook.all()[form.cleaned_data['contact_book']])
                except Contact.DoesNotExist:

                    contact = Contact.objects.create(number=true_number,
                        contactBook=user.contactBook.all()[form.cleaned_data['contact_book']])

                contacts.append(contact)

                if form.cleaned_data['media_url']:
                    try:
                        response = client.messages.create(
                            to=number,
                            messaging_service_sid=SILO_MESSAGING_ID,
                            body=form.cleaned_data['body'],
                            media_url=form.cleaned_data['media_url'])
                    # TODO: get the exceptions done properly
                    except e:
                        return Response({'error': 'error'})
                else:
                    try:
                        response = client.messages.create(
                                        to=number,
                                        status_callback=TWILIO_STATUS_CALLBACK,
                                        messaging_service_sid=SILO_MESSAGING_ID,
                                        body=form.cleaned_data['body'])
                    # TODO: get the exceptions done properly
                    except TwilioRestException as e:
                        return Response({'error': 'error', 'status': 400}, status=400)

                twilio_responses.append(response)
            
                # TODO: get response.sid correct
                new_message = Message.objects.create(
                    to=contact,
                    sender=user,
                    body=form.cleaned_data['body'],
                    media_url=form.cleaned_data['media_url'],
                    twilio_sid=response.sid,
                )

            new_message_serialized = MessagesSerializer(new_message)

            return Response({'success': 'Phone number sent!', 'message': new_message_serialized.data, 'status': 200})
        else:
            return Response({'error': form.errors.as_json(), 'status': 400}, status=400)

    def list(self, request):
        """
        Grabs a list of all the users & returns it with the last message sent.
        """

        if request.user.is_authenticated():
            user = request.user
        else:
            return Response({'error': 'User not logged in'}, status=403)

        contact_book = user.contactBook.all().first()
        userList = []
        seen_messages = {}
        for contact in contact_book.contacts.all():
            messages = contact.messages.all()
            group_messages = contact.group_messages.all()
            last_message = messages.last()
            last_group_message = group_messages.last()
            if len(messages) > 0 and last_message not in seen_messages:
                userList.append(last_message)
                seen_messages[last_message] = True

            if len(group_messages) > 0:
                userList.append(last_group_message)
        userList.sort(key=lambda item:item.time_sent, reverse=True)
        userList_serialized = UserListSerializer(userList, many=True)
        return Response({'userList': userList_serialized.data})

    def retrieve(self, request, pk):
        """
        Grabs the list of specific messages
        """

        # TODO: only get a range of messages (message 1-10), and then load them as we go higher, not all

        if request.user.is_authenticated():
            user = request.user
        else:
            return Response({'error': 'User not logged in'}, status=403)

        contact_book = user.contactBook.all().first()
        numbers = pk.split(',')
        contacts = []
        for number in numbers:
            try:
                contact = contact_book.contacts.get(number=number)
                contacts.append(contact)
            except Contact.DoesNotExist:
                return Response({'error': 'Contact does not exist', 'status': 400})

        filtered = Message.objects.filter(to=contacts[0])
        for contact in contacts[1:]:
            filtered = filtered.filter(to=contact)

        # messages = contact.messages.all().order_by('time_sent')
        serialized_messages = MessagesSerializer(filtered.order_by('time_sent'), many=True)
        return Response({'messages': serialized_messages.data})


