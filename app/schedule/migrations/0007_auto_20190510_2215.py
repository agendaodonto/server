# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-11 01:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_auto_20181002_0055'),
    ]

    operations = [
        migrations.CreateModel(
            name='DentalPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100, verbose_name='Nome do convênio')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='patient',
            name='dental_plan',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='schedule.DentalPlan'),
        ),
    ]
