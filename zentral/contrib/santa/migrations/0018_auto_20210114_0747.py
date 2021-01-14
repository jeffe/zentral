# Generated by Django 2.2.17 on 2021-01-14 07:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('santa', '0017_auto_20200818_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='enable_sysx_cache',
            field=models.BooleanField(default=False, help_text='When enabled, a self-managed cache for decision responses will be used to help improve performance when running Santa as a system extension alongside another system extension.', verbose_name='Enable system extension cache'),
        ),
        migrations.AddField(
            model_name='configuration',
            name='full_sync_interval',
            field=models.IntegerField(default=600, help_text='The max time to wait in seconds before performing a full sync with the server. Minimum: 60s, hardcoded in Santa.', validators=[django.core.validators.MinValueValidator(60), django.core.validators.MaxValueValidator(86400)]),
        ),
    ]
