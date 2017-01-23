# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-23 12:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20170123_0429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roster',
            name='id',
        ),
        migrations.AlterField(
            model_name='roster',
            name='team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='base.Team'),
        ),
    ]