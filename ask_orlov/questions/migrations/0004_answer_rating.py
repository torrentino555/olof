# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-22 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20170522_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='rating',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
