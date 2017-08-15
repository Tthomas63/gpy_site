# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 21:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('gpy_main', '0006_auto_20170815_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='UlxDataStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UlxUserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(max_length=50)),
                ('steam_id', models.CharField(max_length=20, unique=True)),
                ('linked_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_data', to='gpy_main.UlxDataStore')),
            ],
        ),
        migrations.AlterField(
            model_name='ulxsecretkey',
            name='value',
            field=models.CharField(default=uuid.UUID('5cea86f1-5f5a-4046-81e7-b3ddd53a859a'), max_length=200),
        ),
        migrations.AddField(
            model_name='ulxdatastore',
            name='secret_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ulx_secret_key', to='gpy_main.UlxSecretKey'),
        ),
        migrations.AddField(
            model_name='steamuser',
            name='user_data',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='gpy_main.UlxUserData'),
        ),
    ]
