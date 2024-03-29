# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 00:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0008_contact_saved'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactbook',
            name='name',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='opt_in_message',
            field=models.TextField(default='Thanks for joining our txt list! Normal carrier txt fees apply. Reply STOP to stop.'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='number',
            field=models.CharField(max_length=17, unique=True),
        ),
    ]
