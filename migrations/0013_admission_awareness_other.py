# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-11-21 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('continuing_education', '0012_auto_20181114_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='admission',
            name='awareness_other',
            field=models.CharField(blank=True, max_length=100, verbose_name='Awareness other'),
        ),
    ]
