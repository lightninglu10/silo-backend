# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 06:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0010_contact_optin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='contact',
            name='groups',
            field=models.ManyToManyField(related_name='contacts', to='contacts.Group'),
        ),
    ]