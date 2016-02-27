# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locality', '0001_initial'),
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(default=None, max_length=1024, null=True, blank=True)),
                ('photo_url', models.ImageField(default=None, null=True, upload_to=b'', blank=True)),
                ('website_url', models.URLField(default=None, null=True, blank=True)),
                ('facebook_url', models.URLField(default=None, null=True, blank=True)),
                ('twitter_url', models.URLField(default=None, null=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('city', models.ForeignKey(related_name='finance_employer_address_city', default=None, blank=True, to='locality.City', null=True)),
                ('state', models.ForeignKey(related_name='finance_employer_address_state', default=None, blank=True, to='locality.State', null=True)),
                ('zip_code', models.ForeignKey(related_name='finance_employer_address_zip_code', default=None, blank=True, to='locality.ZipCode', null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AlterModelOptions(
            name='personbenefactor',
            options={'ordering': ('last_name', 'first_name', 'middle_name', 'benefactor_locality__name', 'benefactor_locality__short_name')},
        ),
        migrations.AlterField(
            model_name='personbenefactor',
            name='occupation',
            field=models.CharField(default=None, max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='personbenefactor',
            name='employer',
            field=models.ForeignKey(default=None, blank=True, to='finance.Employer', null=True),
        ),
    ]
