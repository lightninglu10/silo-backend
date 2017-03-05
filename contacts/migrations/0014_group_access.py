# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 20:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contacts', '0013_userprofile_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='access',
            field=models.ManyToManyField(related_name='group_access', to=settings.AUTH_USER_MODEL),
        ),
    ]
