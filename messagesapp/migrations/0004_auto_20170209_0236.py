# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 02:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_auto_20170207_0303'),
        ('messagesapp', '0003_message_me'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='to',
        ),
        migrations.AddField(
            model_name='message',
            name='to',
            field=models.ManyToManyField(related_name='messages', to='contacts.Contact'),
        ),
    ]
