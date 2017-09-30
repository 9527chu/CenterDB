# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-24 08:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0010_auto_20170924_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='asset',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='server', to='repository.Asset'),
        ),
    ]
