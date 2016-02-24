# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import locality.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=128, null=True, blank=True)),
                ('short_name', models.CharField(default=None, max_length=32, null=True, blank=True)),
            ],
            options={
                'ordering': ('name', 'short_name'),
                'verbose_name_plural': 'localities',
            },
            bases=(models.Model, locality.models.ReverseLookupStringMixin),
        ),
        migrations.CreateModel(
            name='ZipCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=128, null=True, blank=True)),
                ('short_name', models.CharField(default=None, max_length=32, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('locality_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='locality.Locality')),
                ('fips_id', models.IntegerField(default=None, null=True, blank=True)),
            ],
            options={
                'ordering': ('state__short_name', 'county', 'name', 'short_name'),
                'verbose_name_plural': 'cities',
            },
            bases=('locality.locality',),
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('locality_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='locality.Locality')),
                ('fips_id', models.IntegerField(default=None, null=True, blank=True)),
            ],
            options={
                'ordering': ('state__short_name', 'name', 'short_name'),
                'verbose_name_plural': 'counties',
            },
            bases=('locality.locality',),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('locality_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='locality.Locality')),
                ('fips_id', models.IntegerField(default=None, null=True, blank=True)),
            ],
            options={
                'ordering': ('short_name', 'name'),
            },
            bases=('locality.locality',),
        ),
        migrations.AddField(
            model_name='zipcode',
            name='city',
            field=models.ForeignKey(default=None, blank=True, to='locality.City', null=True),
        ),
        migrations.AddField(
            model_name='zipcode',
            name='county',
            field=models.ForeignKey(default=None, blank=True, to='locality.County', null=True),
        ),
        migrations.AddField(
            model_name='zipcode',
            name='state',
            field=models.ForeignKey(default=None, blank=True, to='locality.State', null=True),
        ),
        migrations.AddField(
            model_name='county',
            name='state',
            field=models.ForeignKey(to='locality.State'),
        ),
        migrations.AddField(
            model_name='city',
            name='county',
            field=models.ForeignKey(default=None, blank=True, to='locality.County', null=True),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='locality.State'),
        ),
    ]
