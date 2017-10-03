# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 08:04
from __future__ import unicode_literals

from django.db import migrations, models
import member.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_type', models.CharField(choices=[('f', 'Facebook'), ('n', 'Naver'), ('g', 'General')], default='g', max_length=1)),
                ('email', models.CharField(max_length=30, unique=True)),
                ('nickname', models.CharField(max_length=15)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', member.models.MyUserManager()),
            ],
        ),
    ]
