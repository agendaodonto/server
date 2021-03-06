# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-09-26 21:52
from __future__ import unicode_literals

from django.db import migrations


def remove_country_code(apps, schema_editor):
    Patient = apps.get_model('schedule', 'Patient')

    for patient in Patient.objects.all():
        patient.phone = patient.phone.replace('+55', '')
        patient.save()


class Migration(migrations.Migration):
    dependencies = [
        ('schedule', '0007_auto_20190510_2215'),
    ]

    operations = [
        migrations.RunPython(remove_country_code),
    ]
