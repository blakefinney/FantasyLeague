# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-23 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20170123_0431'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='name',
            field=models.CharField(default=b'unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.CharField(default=b'UNK', max_length=5),
        ),
    ]