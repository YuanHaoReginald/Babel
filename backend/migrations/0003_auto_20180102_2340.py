# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-02 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispute',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]