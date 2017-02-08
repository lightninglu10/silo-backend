from rest_framework import serializers
from .models import Message
from contacts.serializers import ContactSerializer

class UserListSerializer(serializers.ModelSerializer):
    """
    Serializes the user list
    """
    to = ContactSerializer()

    class Meta:
        fields = ('body', 'to', 'media_url', 'time_sent')
        model = Message

class MessagesSerializer(serializers.ModelSerializer):
    """
    Serializes each individual message
    """

    class Meta:
        fields = ('body', 'media_url', 'time_sent', 'me')
        model = Message