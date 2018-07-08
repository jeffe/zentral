# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-23 12:14
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0037_auto_20180213_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='metabusinessunit',
            name='dashboard_osx_app_bundle_id_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=list, size=None),
        ),
        migrations.AddField(
            model_name='metabusinessunit',
            name='dashboard_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='inventory.Source'),
        ),
    ]