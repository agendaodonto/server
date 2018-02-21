# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-21 01:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20170903_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('message_id', models.CharField(max_length=30, unique=True, verbose_name='Identificador Único')),
                ('content', models.CharField(max_length=300, verbose_name='Conteúdo')),
                ('date', models.DateTimeField(null=True, verbose_name='Data da mensagem')),
                ('status', models.CharField(max_length=15, verbose_name='Status')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Patient')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
