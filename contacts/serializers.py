from rest_framework import serializers
from .models import Contact, Group, UserProfile
from django.contrib.auth.models import User

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group

class ContactSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = obj.first_name + " " + obj.last_name

        return name.strip()

    class Meta:
        fields = '__all__'
        model = Contact

class UserSerializer(serializers.ModelSerializer):

    contacts = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return 200

    def get_contacts(self, obj):
        # TODO: manage contact book
        contacts = obj.user.contactBook.first().contacts.filter(saved=True)
        contacts_serialized = ContactSerializer(contacts, many=True)
        return contacts_serialized.data

    class Meta:
        fields = '__all__'
        model = UserProfile
