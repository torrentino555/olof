# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-22 20:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_auto_20170522_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='Null', max_length=254),
        ),
        migrations.AddField(
            model_name='profile',
            name='login',
            field=models.CharField(default='unknown', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(default='unknown', max_length=50),
        ),
    ]
