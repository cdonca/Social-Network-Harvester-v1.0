# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-24 23:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Youtube', '0012_auto_20160823_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ytcomment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posted_comments', to='Youtube.YTChannel'),
        ),
    ]