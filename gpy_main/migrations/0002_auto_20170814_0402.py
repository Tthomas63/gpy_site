# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-14 04:02
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('gpy_main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ulxsecretkey',
            name='value',
            field=models.CharField(default=uuid.UUID('0ee626b3-ca47-474b-8895-694218368b83'), max_length=200),
        ),
    ]
