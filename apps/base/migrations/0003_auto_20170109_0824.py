# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-09 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20170109_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roster',
            name='BENCH',
            field=models.CharField(default=b'[]', max_length=150),
        ),
    ]
