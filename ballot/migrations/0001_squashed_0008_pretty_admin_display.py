# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [(b'ballot', '0001_first'), (b'ballot', '0002_pretty_admin_display'), (b'ballot', '0003_pretty_admin_display'), (b'ballot', '0004_pretty_admin_display'), (b'ballot', '0005_pretty_admin_display'), (b'ballot', '0006_pretty_admin_display'), (b'ballot', '0007_pretty_admin_display'), (b'ballot', '0008_pretty_admin_display')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ballot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b"The candidate's full name.", max_length=255)),
                ('biography', models.TextField()),
                ('photo_url', models.ImageField(upload_to=b'')),
                ('candidate_url', models.URLField(help_text=b"URL for the candidate's official website.")),
                ('facebook_url', models.URLField(help_text=b"URL for the candidate's Facebook page.")),
                ('twitter_url', models.URLField(help_text=b"URL for the candidate's Twitter page.")),
            ],
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contest_type', models.CharField(help_text=b'\n        Office if the contest is for a person, referendum if the contest is for an issue.\n        ', max_length=1)),
                ('ballot', models.ForeignKey(to='ballot.Ballot')),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(help_text=b'The day of the election.')),
                ('election_type', models.CharField(help_text=b'\n        Specifies the highest controlling authority for the election\n        (e.g., federal, state, county, city, town, etc.)\n        ', max_length=2, choices=[(b'FE', b'Federal'), (b'ST', b'State'), (b'CO', b'County'), (b'CI', b'City')])),
            ],
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of the juristiction.', max_length=255)),
                ('locality_type', models.CharField(help_text=b'One of county, city, township, borough, parish, village, or region.', max_length=2, choices=[(b'CO', b'County'), (b'CI', b'City')])),
                ('netfile_agency', models.CharField(help_text=b'The netfile agency administering the elections in this locality.', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Precinct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b"The precinct's name or number.", max_length=30)),
                ('number', models.CharField(help_text=b"the precinct's number e.g., 32 or 32A (alpha characters are legal).", max_length=5)),
                ('locality', models.ForeignKey(to='ballot.Locality')),
            ],
        ),
        migrations.CreateModel(
            name='Referendum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255, blank=True)),
                ('brief', models.TextField(blank=True)),
                ('full_text', models.TextField(blank=True)),
                ('pro_statement', models.TextField(blank=True)),
                ('con_statement', models.TextField(blank=True)),
                ('contest', models.ForeignKey(blank=True, to='ballot.Contest', null=True)),
                ('number', models.CharField(default='', help_text=b"The referendum's number or letter.", max_length=5)),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='contest',
            field=models.ForeignKey(blank=True, to='ballot.Contest', null=True),
        ),
        migrations.AddField(
            model_name='ballot',
            name='election',
            field=models.ForeignKey(to='ballot.Election'),
        ),
        migrations.AddField(
            model_name='ballot',
            name='locality',
            field=models.ForeignKey(to='ballot.Locality'),
        ),
        migrations.AlterField(
            model_name='locality',
            name='netfile_agency',
            field=models.CharField(help_text=b'The netfile agency administering the elections in this locality.', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='locality',
            name='netfile_agency',
            field=models.CharField(help_text=b'The netfile agency administering the elections in this locality.', max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='biography',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='candidate_url',
            field=models.URLField(help_text=b"URL for the candidate's official website.", blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='facebook_url',
            field=models.URLField(help_text=b"URL for the candidate's Facebook page.", blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='photo_url',
            field=models.ImageField(upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='twitter_url',
            field=models.URLField(help_text=b"URL for the candidate's Twitter page.", blank=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='contest_type',
            field=models.CharField(help_text=b'\n        Office if the contest is for a person, referendum if the contest is for an issue.\n        ', max_length=1, choices=[(b'R', b'Referendum'), (b'O', b'Office')]),
        ),
        migrations.AddField(
            model_name='contest',
            name='name',
            field=models.CharField(default='Mayor', help_text=b'The referendum number or the name of the office.', max_length=255),
            preserve_default=False,
        ),
    ]
