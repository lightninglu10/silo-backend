from django.db import models
from django.contrib.auth.models import User

class ContactBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contactBook')
    name = models.TextField(default='')    

class UserProfile(models.Model):
    """
    Profile for the registered user account. Person who sends out messages.
    """
    first_name = models.TextField(default='')
    last_name = models.TextField(default='')
    number = models.CharField(max_length=17, primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    opt_in_message = models.TextField(default='Thanks for joining our txt list! Normal carrier txt fees apply. Reply STOP to stop.')

    def __str__(self):
        return 'Name: {}'.format(self.first_name + " " + self.last_name)

class Contact(models.Model):
    """
    Model for the contacts in the contact book
    """
    number = models.CharField(max_length=17, unique=True)
    saved = models.BooleanField(default=False)
    first_name = models.TextField(default='', blank=True, null=True)
    last_name = models.TextField(default='', blank=True, null=True)
    email = models.EmailField(max_length=70, blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True, default='')
    contactBook = models.ForeignKey(ContactBook, on_delete=models.CASCADE, related_name='contacts')

    def __str__(self):
        return 'Number: {},\n\nFirst: {},\n\n Last: {},\n\n'.format(self.number, self.first_name, self.last_name)