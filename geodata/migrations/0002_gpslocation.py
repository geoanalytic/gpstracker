# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 23:39
from __future__ import unicode_literals

import datetime
import django.contrib.gis.db.models.fields
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gpslocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastupdate', models.DateTimeField(auto_now_add=True)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('speed', models.IntegerField(default=0)),
                ('direction', models.IntegerField(default=0)),
                ('distance', models.FloatField(default=0.0)),
                ('gpstime', models.DateTimeField(blank=True, default=datetime.datetime(2001, 1, 1, 1, 1, 1, tzinfo=utc))),
                ('locationmethod', models.CharField(blank=True, default='', max_length=50)),
                ('username', models.CharField(blank=True, default='', max_length=50)),
                ('phonenumber', models.CharField(blank=True, default='', max_length=50)),
                ('sessionid', models.CharField(blank=True, default='', max_length=50)),
                ('accuracy', models.IntegerField(default=0)),
                ('extrainfo', models.CharField(blank=True, default='', max_length=255)),
                ('eventtype', models.CharField(blank=True, default='', max_length=50)),
                ('mpoint', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Gps Locations',
            },
        ),
    ]
