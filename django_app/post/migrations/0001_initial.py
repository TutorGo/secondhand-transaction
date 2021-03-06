# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-10 07:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('e', '전자기기'), ('fc', '패션의류'), ('fg', '패션잡화'), ('cb', '화장품/미용'), ('s', '스포츠/레저'), ('b', '도서')], max_length=2)),
                ('sell_or_buy', models.CharField(choices=[('s', 'sell'), ('b', 'byu')], max_length=4)),
                ('price', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('image_1', models.ImageField(default=None, upload_to='post/%Y/%m/%d')),
                ('image_2', models.ImageField(blank=True, default=None, upload_to='post/%Y/%m/%d')),
                ('image_3', models.ImageField(blank=True, default=None, upload_to='post/%Y/%m/%d')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
