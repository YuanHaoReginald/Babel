# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-27 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20171126_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translator',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]