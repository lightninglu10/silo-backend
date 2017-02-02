from django.shortcuts import render
from django import forms

# DRF
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.views import APIView

# Twilio
from twilio.rest import Client

account_sid = "AC416bdd1fded5fa067f76ecd4381632d5"
auth_token = "f15d3e7ae578b4ec75a15b5fa41e1b0f"
SILO_MESSAGING_ID = 'MGb015f9b8cea6900c64af4b2d5f7fb6bc'

client = Client(account_sid, auth_token)

class MessageForm(forms.form):
    

class MessagesView(generics.GenericAPIView):
    """
    View to send messages via twilio
    """
    def post(self, request):

        client.messages.create(
            to=,
            messagingServiceSid=SILO_MESSAGING_ID,
            body="This is the ship that made the Kessel Run in fourteen parsecs?",
            media_url="https://c1.staticflickr.com/3/2899/14341091933_1e92e62d12_b.jpg")