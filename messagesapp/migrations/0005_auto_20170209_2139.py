# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 21:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_auto_20170207_0303'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('messagesapp', '0004_auto_20170209_0236'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(blank=True, max_length=1600, null=True)),
                ('media_url', models.TextField(blank=True, default=None, null=True)),
                ('time_sent', models.DateTimeField(auto_now_add=True)),
                ('me', models.BooleanField(default=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupmessage_messages', to=settings.AUTH_USER_MODEL)),
                ('to', models.ManyToManyField(related_name='group_messages', to='contacts.Contact')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='message',
            name='to',
        ),
        migrations.AddField(
            model_name='message',
            name='to',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='contacts.Contact'),
            preserve_default=False,
        ),
    ]
