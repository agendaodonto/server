# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-28 02:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20170903_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='dentist',
            name='device_token',
            field=models.CharField(default=None, max_length=100, null=True, verbose_name='Token do dispositivo'),
        ),
    ]
