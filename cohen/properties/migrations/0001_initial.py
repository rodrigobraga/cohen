# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 12:09
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('address', models.CharField(max_length=255)),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('image', models.ImageField(upload_to='properties')),
                ('is_available', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('property_type', models.CharField(choices=[('house', 'House'), ('apartment', 'Apartment/Flat'), ('townhouse', 'Townhouse'), ('commercial', 'Commercial/Industrial')], default='house', max_length=24)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'properties',
                'ordering': ['-created_date', '-updated_date', 'title'],
            },
        ),
    ]
