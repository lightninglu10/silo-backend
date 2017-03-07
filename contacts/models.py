from django.db import models
from django.contrib.auth.models import User

class ContactBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contactBook')
    name = models.TextField(default='')

class Group(models.Model):
    """
    Grouping contacts together
    """
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group')
    access = models.ManyToManyField(User, related_name='group_access')

    def __str__(self):
        return 'Name: {}, User: {}, User Email: {}'.format(self.name, self.user.first_name + self.user.last_name, self.user.email)

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
    website = models.CharField(max_length=200, blank=True, null=True)
    opt_in_message = models.TextField(default='Thanks for joining our txt list! Normal carrier txt fees apply. Reply STOP to stop.')

    def __str__(self):
        return 'Name: {}'.format(self.first_name + " " + self.last_name)

class Contact(models.Model):
    """
    Model for the contacts in the contact book
    """
    number = models.CharField(max_length=17)
    saved = models.BooleanField(default=False)
    optin = models.BooleanField(default=True)
    first_name = models.TextField(default='', blank=True, null=True)
    last_name = models.TextField(default='', blank=True, null=True)
    email = models.EmailField(max_length=70, blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True, default='')
    contactBook = models.ForeignKey(ContactBook, on_delete=models.CASCADE, related_name='contacts')
    groups = models.ManyToManyField(Group, related_name='contacts')

    def __str__(self):
        return 'Number: {},\n\nFirst: {},\n\n Last: {},\n\n'.format(self.number, self.first_name, self.last_name)
