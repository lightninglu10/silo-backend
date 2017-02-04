from django.db import models
from django.contrib.auth.models import User

class ContactBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contactBook')

class Contact(models.Model):
    number = models.CharField(max_length=17, primary_key=True, unique=True)
    first_name = models.TextField(default='', blank=True, null=True)
    last_name = models.TextField(default='', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    contactBook = models.ForeignKey(ContactBook, on_delete=models.CASCADE, related_name='contacts')

    def __str__(self):
        return 'Number: {},\n\nFirst: {},\n\n Last: {},\n\n'.format(self.number, self.first_name, self.last_name)