from rest_framework import serializers
from .models import Message
from contacts.serializers import ContactSerializer

class UserListSerializer(serializers.ModelSerializer):
    to = ContactSerializer()

    class Meta:
        fields = ('body', 'to', 'media_url')
        model = Message