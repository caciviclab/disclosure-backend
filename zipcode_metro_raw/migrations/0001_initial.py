# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ZipCodeMetro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zip_code', models.IntegerField(db_column='ZipCode')),
                ('state_name', models.CharField(max_length=1024, db_column='StateName')),
                ('county_name', models.CharField(max_length=1024, db_column='CountyName')),
                ('city_name', models.CharField(max_length=1024, db_column='CityName')),
                ('psa_code', models.IntegerField(db_column='PSACode')),
                ('psa_title', models.CharField(max_length=1024, db_column='PSATitle')),
            ],
            options={
                'db_table': 'ZIPCODE_METRO',
                'verbose_name': 'ZIPCODE_METRO',
                'verbose_name_plural': 'ZIPCODE_METRO',
            },
        ),
    ]
