# Generated by Django 2.2.10 on 2020-03-05 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm', '0033_auto_20200305_2322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicecommand',
            name='dictionary',
        ),
        migrations.AlterField(
            model_name='devicecommand',
            name='body',
            field=models.TextField(),
        ),
    ]
