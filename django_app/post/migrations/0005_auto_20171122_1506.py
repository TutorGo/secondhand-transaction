# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-22 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20171115_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
