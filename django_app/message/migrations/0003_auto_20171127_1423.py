# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-27 05:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0002_message_visible'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-pk']},
        ),
    ]
