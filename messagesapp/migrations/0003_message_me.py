# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagesapp', '0002_message_twilio_sid'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='me',
            field=models.BooleanField(default=True),
        ),
    ]