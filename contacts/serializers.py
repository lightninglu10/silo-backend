from rest_framework import serializers
from .models import Contact
from django.contrib.auth.models import User

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('number', 'first_name', 'last_name', 'number', 'notes', 'email')
        model = Contact

class UserSerializer(serializers.ModelSerializer):

    contacts = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return 200

    def get_contacts(self, obj):
        # TODO: manage contact book
        contacts = obj.contactBook.first().contacts.all()
        contacts_serialized = ContactSerializer(contacts, many=True)
        return contacts_serialized.data

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'contacts', 'status')
        model = User
