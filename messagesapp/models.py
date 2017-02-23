from django.db import models
from contacts.models import Contact
from django.contrib.auth.models import User

# Channels for websockets
from channels import Group
import json

class MessageBase(models.Model):
    STATUS_CHOICES = (
        ('Q', 'queued'),
        ('F', 'failed'),
        ('S', 'sent'),
        ('D', 'delivered'),
        ('U', 'undelivered'),
    )
    body = models.CharField(max_length=1600, blank=True, null=True)
    delivery_status = models.CharField(default='Q', max_length=1, choices=STATUS_CHOICES)
    media_url = models.TextField(default=None, blank=True, null=True)
    time_sent = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_messages')
    me = models.BooleanField(default=True)
    

    class Meta:
        abstract = True

    def status(self, status):
        if status == 'queued':
            self.delivery_status = 'Q'
        elif status == 'failed':
            self.delivery_status = 'F'
            Group('status').send({'text': json.dumps({'status': 'failed', 'message': ''})})
        elif status == 'delivered':
            self.delivery_status = 'D'
        elif status == 'undelivered':
            self.delivery_status = 'U'
        self.save()
        return self

class Message(MessageBase):
    """
    The model to save all one to one messages passed through.
    """
    to = models.ForeignKey(Contact, related_name='messages')
    twilio_sid = models.CharField(max_length=256)

    def __str__(self):
        return 'To: {}\n, Sender: {}\n, Body: {}\n'.format(self.to, self.sender, self.body)

class GroupMessage(MessageBase):
    """
    The model to save all group messages. Probably not possible at the moment.
    """
    to = models.ManyToManyField(Contact, related_name='group_messages')
    twilio_sid = models.CharField