from rest_framework import serializers
from .models import Message
from contacts.serializers import ContactSerializer

class UserListSerializer(serializers.ModelSerializer):
    """
    Serializes the user list
    """
    to = serializers.SerializerMethodField()

    def get_to(self, obj):
        contacts = obj.to
        contacts_serialized = ContactSerializer(contacts)
        return contacts_serialized.data

    class Meta:
        fields = ('body', 'to', 'media_url', 'time_sent', 'id')
        model = Message

class MessagesSerializer(serializers.ModelSerializer):
    """
    Serializes each individual message
    """

    to = ContactSerializer()

    class Meta:
        fields = '__all__'
        model = Message