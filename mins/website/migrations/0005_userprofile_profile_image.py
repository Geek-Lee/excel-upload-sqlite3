# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-05 01:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20170705_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.FileField(blank=True, null=True, upload_to='profile_image'),
        ),
    ]
