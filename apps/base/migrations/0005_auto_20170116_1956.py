# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-16 19:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20170116_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchup',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='base.Team'),
        ),
        migrations.AlterField(
            model_name='matchup',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='base.Team'),
        ),
    ]
