from django.db import models
from contacts.models import Contact
from django.contrib.auth.models import User

class Message(models.Model):
    """
    The model to save all messages passed through.
    """
    body = models.CharField(max_length=1600, blank=True, null=True)
    media_url = models.TextField(default=None, blank=True, null=True)
    time_sent = models.DateTimeField(auto_now_add=True)
    to = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='messages')
    from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')