# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-04 14:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Video',
        ),
    ]