# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-10 16:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_auto_20170907_0537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manufactory',
            old_name='manufactory',
            new_name='name',
        ),
    ]