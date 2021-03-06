# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-01 17:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_player_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='FantasyPoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=0)),
                ('week1', models.FloatField(default=None, null=True)),
                ('week2', models.FloatField(default=None, null=True)),
                ('week3', models.FloatField(default=None, null=True)),
                ('week4', models.FloatField(default=None, null=True)),
                ('week5', models.FloatField(default=None, null=True)),
                ('week6', models.FloatField(default=None, null=True)),
                ('week7', models.FloatField(default=None, null=True)),
                ('week8', models.FloatField(default=None, null=True)),
                ('week9', models.FloatField(default=None, null=True)),
                ('week10', models.FloatField(default=None, null=True)),
                ('week11', models.FloatField(default=None, null=True)),
                ('week12', models.FloatField(default=None, null=True)),
                ('week13', models.FloatField(default=None, null=True)),
                ('week14', models.FloatField(default=None, null=True)),
                ('week15', models.FloatField(default=None, null=True)),
                ('week16', models.FloatField(default=None, null=True)),
                ('week17', models.FloatField(default=None, null=True)),
                ('player', models.ForeignKey(default=b'', on_delete=django.db.models.deletion.CASCADE, to='base.Player')),
            ],
        ),
    ]
