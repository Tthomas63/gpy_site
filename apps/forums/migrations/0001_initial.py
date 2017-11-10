# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-25 23:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('servers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Forum logo')),
                ('server', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_forums', to='servers.Server')),
            ],
        ),
        migrations.CreateModel(
            name='ForumCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Forum Category Logo')),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='forums.Forum')),
            ],
        ),
        migrations.CreateModel(
            name='ForumReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=600)),
                ('posted', models.DateField(auto_now_add=True)),
                ('last_edited', models.DateField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_replies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ForumThread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=600)),
                ('posted', models.DateField(auto_now_add=True)),
                ('last_edited', models.DateField(blank=True, null=True)),
                ('last_reply', models.DateField(blank=True, null=True)),
                ('locked', models.BooleanField(default=False)),
                ('sticky', models.BooleanField(default=False)),
                ('hidden', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threads', to='forums.ForumCategory')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_threads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='forumreply',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='forums.ForumThread'),
        ),
    ]
