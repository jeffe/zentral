# Generated by Django 2.2.9 on 2020-02-26 14:33

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Realm',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('enabled_for_login', models.BooleanField(default=False)),
                ('backend', models.CharField(editable=False, max_length=255)),
                ('config', django.contrib.postgres.fields.jsonb.JSONField(default=dict, editable=False)),
                ('username_claim', models.CharField(max_length=255)),
                ('email_claim', models.CharField(blank=True, max_length=255)),
                ('first_name_claim', models.CharField(blank=True, max_length=255)),
                ('last_name_claim', models.CharField(blank=True, max_length=255)),
                ('full_name_claim', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RealmUser',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('claims', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('first_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('full_name', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('realm', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='realms.Realm')),
            ],
            options={
                'unique_together': {('realm', 'username')},
            },
        ),
        migrations.CreateModel(
            name='RealmAuthenticationSession',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('callback', models.CharField(max_length=255)),
                ('callback_kwargs', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('realm', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='realms.Realm')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='realms.RealmUser')),
            ],
        ),
    ]
