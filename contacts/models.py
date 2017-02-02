from django.db import models

class Contact(models.Model):
    number = models.CharField(max_length=17)
    first_name = models.TextField()
    last_name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)