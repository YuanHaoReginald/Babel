# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-12-07 15:11
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=1000)),
                ('status', models.IntegerField(default=0)),
                ('order', models.IntegerField()),
                ('testTextFinished', models.TextField(max_length=600, null=True)),
                ('scores', models.IntegerField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('submission', models.FileField(max_length=50, null=True, upload_to='')),
                ('experience', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CommonUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('telephone', models.CharField(max_length=20, null=True, unique=True)),
                ('avatar', models.ImageField(max_length=256, null=True, upload_to='')),
                ('utype', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Dispute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employerStatement', models.TextField(max_length=1000, null=True)),
                ('translatorStatement', models.TextField(max_length=1000, null=True)),
                ('status', models.IntegerField()),
                ('adminStatement', models.TextField(max_length=1000, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Assignment')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('languageType', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licenseType', models.IntegerField()),
                ('licenseImage', models.ImageField(max_length=256, null=True, upload_to='')),
                ('description', models.CharField(max_length=100, null=True)),
                ('adminVerify', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=512)),
                ('fileUrl', models.FileField(max_length=256, upload_to='')),
                ('fileType', models.IntegerField()),
                ('publishTime', models.DateTimeField()),
                ('ddlTime', models.DateTimeField()),
                ('tags', models.CharField(max_length=128, null=True)),
                ('language', models.IntegerField(null=True)),
                ('requirementsLicense', models.IntegerField(null=True)),
                ('requirementsLevel', models.IntegerField(null=True)),
                ('testText', models.TextField(max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('commonuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.CommonUser')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('backend.commonuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('commonuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.CommonUser')),
                ('level', models.IntegerField(default=0)),
                ('alipayNumber', models.CharField(max_length=30, null=True)),
                ('wechatNumber', models.CharField(max_length=30, null=True)),
                ('experience', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('backend.commonuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Translator',
            fields=[
                ('commonuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.CommonUser')),
                ('level', models.IntegerField(default=0)),
                ('alipayNumber', models.CharField(max_length=30, null=True)),
                ('wechatNumber', models.CharField(max_length=30, null=True)),
                ('experienceNumber', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('backend.commonuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Task'),
        ),
        migrations.AddField(
            model_name='task',
            name='employerId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partyA', to='backend.Employer'),
        ),
        migrations.AddField(
            model_name='license',
            name='belonger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Translator'),
        ),
        migrations.AddField(
            model_name='language',
            name='TranslatorId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Translator'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='translator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partyB', to='backend.Translator'),
        ),
    ]
