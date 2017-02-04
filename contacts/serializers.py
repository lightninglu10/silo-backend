from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('number', 'first_name', 'last_name')
        model = Contact