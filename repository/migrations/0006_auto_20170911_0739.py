# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-11 07:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_auto_20170910_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessunit',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='c', to='repository.UserGroup', verbose_name='\u4e1a\u52a1\u8054\u7cfb\u4eba'),
        ),
        migrations.AlterField(
            model_name='businessunit',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='m', to='repository.UserGroup', verbose_name='\u7cfb\u7edf\u7ba1\u7406\u5458'),
        ),
    ]
