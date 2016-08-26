# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-25 20:23
from __future__ import unicode_literals

import SocialNetworkHarvester_v1p0.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Youtube', '0015_auto_20160824_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subsription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recorded_time', models.DateTimeField(default=SocialNetworkHarvester_v1p0.models.djangoNow)),
                ('ended', models.DateTimeField(null=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='Youtube.YTChannel')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to='Youtube.YTChannel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]