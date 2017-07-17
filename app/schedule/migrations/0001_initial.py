# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-13 02:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dentist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=50, verbose_name='Nome')),
                ('last_name', models.CharField(max_length=50, verbose_name='Sobrenome')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('cro', models.CharField(max_length=15, verbose_name='CRO')),
                ('cro_state', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='Estado Emissor')),
                ('sex', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, verbose_name='Sexo')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Admin')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Super Usuário')),
            ],
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
                ('message', models.CharField(max_length=160, verbose_name='Mensagem')),
                ('time_delta', models.FloatField(default=1.0, verbose_name='Tempo para notificar (horas)')),
                ('dentists', models.ManyToManyField(blank=True, related_name='dentists', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Clínica',
                'verbose_name_plural': 'Clínicas',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=30, verbose_name='Nome')),
                ('last_name', models.CharField(max_length=30, verbose_name='Sobrenome')),
                ('phone', models.CharField(max_length=14, verbose_name='Telefone')),
                ('sex', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, verbose_name='Sexo')),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Clinic')),
            ],
            options={
                'verbose_name': 'Paciente',
                'verbose_name_plural': 'Pacientes',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date', models.DateTimeField(verbose_name='Data')),
                ('duration', models.IntegerField(verbose_name='Duração')),
                ('notification_status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Success'), (2, 'Expired'), (3, 'Failed')], default=0, verbose_name='Status Notificação')),
                ('notification_attempts', models.IntegerField(default=0, verbose_name='Tentativas Notificação')),
                ('status',
                 models.IntegerField(choices=[(0, 'Pendente'), (1, 'Confirmado'), (2, 'Faltou'), (3, 'Cancelou')],
                                     default=0, verbose_name='Status do agendamento')),
                ('dentist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Patient')),
            ],
            options={
                'verbose_name': 'Agendamento',
                'verbose_name_plural': 'Agendamentos',
            },
        ),
        migrations.AlterUniqueTogether(
            name='dentist',
            unique_together=set([('cro', 'cro_state')]),
        ),
    ]
