# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-07 19:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20171208_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='fileUrl',
            field=models.FileField(max_length=256, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='task',
            name='languageOrigin',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='task',
            name='publishTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
