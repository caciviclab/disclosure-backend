# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import locality.models


class Migration(migrations.Migration):

    dependencies = [
        ('locality', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ballot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=None, help_text=b'The day of the election.', null=True)),
                ('locality', models.ForeignKey(to='locality.Locality')),
            ],
            options={
                'ordering': ('date', 'locality__name', 'locality__short_name'),
            },
        ),
        migrations.CreateModel(
            name='BallotItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contest_type', models.CharField(help_text=b'Office if the contest is for a person, referendum if the contest is for an issue.', max_length=1, choices=[(b'R', b'Referendum'), (b'O', b'Office')])),
            ],
            options={
                'ordering': ('ballot__date', 'ballot__locality__short_name', 'ballot__locality__name'),
            },
            bases=(models.Model, locality.models.ReverseLookupStringMixin),
        ),
        migrations.CreateModel(
            name='BallotItemSelection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ('ballot_item__ballot__date', 'ballot_item__ballot__locality__short_name', 'ballot_item__ballot__locality__name'),
            },
            bases=(models.Model, locality.models.ReverseLookupStringMixin),
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The office name.', max_length=255)),
                ('description', models.CharField(help_text='The office description.', max_length=1024)),
                ('locality', models.ForeignKey(to='locality.Locality')),
            ],
            options={
                'ordering': ('locality__short_name', 'locality__name', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo_url', models.ImageField(default=None, null=True, upload_to=b'', blank=True)),
                ('website_url', models.URLField(default=None, null=True, blank=True)),
                ('facebook_url', models.URLField(default=None, null=True, blank=True)),
                ('twitter_url', models.URLField(default=None, null=True, blank=True)),
                ('name', models.CharField(help_text='The party name.', max_length=255)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'parties',
            },
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('ballotitemselection_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ballot.BallotItemSelection')),
                ('photo_url', models.ImageField(default=None, null=True, upload_to=b'', blank=True)),
                ('website_url', models.URLField(default=None, null=True, blank=True)),
                ('facebook_url', models.URLField(default=None, null=True, blank=True)),
                ('twitter_url', models.URLField(default=None, null=True, blank=True)),
                ('first_name', models.CharField(default=None, max_length=255, null=True, help_text="The person's first name.")),
                ('middle_name', models.CharField(default=None, max_length=255, null=True, help_text="The person's middle name.", blank=True)),
                ('last_name', models.CharField(help_text="The person's last name.", max_length=255)),
            ],
            options={
                'ordering': ('ballot_item__ballot__date', 'ballot_item__ballot__locality__short_name', 'ballot_item__ballot__locality__name', 'office_election__office__name', 'last_name', 'first_name', 'middle_name'),
            },
            bases=('ballot.ballotitemselection', models.Model),
        ),
        migrations.CreateModel(
            name='OfficeElection',
            fields=[
                ('ballotitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ballot.BallotItem')),
                ('office', models.ForeignKey(to='ballot.Office')),
            ],
            options={
                'ordering': ('ballot__date', 'ballot__locality__short_name', 'ballot__locality__name', 'office__name'),
            },
            bases=('ballot.ballotitem',),
        ),
        migrations.CreateModel(
            name='Referendum',
            fields=[
                ('ballotitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ballot.BallotItem')),
                ('photo_url', models.ImageField(default=None, null=True, upload_to=b'', blank=True)),
                ('website_url', models.URLField(default=None, null=True, blank=True)),
                ('facebook_url', models.URLField(default=None, null=True, blank=True)),
                ('twitter_url', models.URLField(default=None, null=True, blank=True)),
                ('title', models.CharField(help_text='The referendum title', max_length=255)),
                ('number', models.CharField(default=None, max_length=5, null=True, help_text="The referendum's number or letter.")),
            ],
            options={
                'ordering': ('ballot__date', 'ballot__locality__short_name', 'ballot__locality__name', 'number', 'title'),
            },
            bases=('ballot.ballotitem', models.Model),
        ),
        migrations.CreateModel(
            name='ReferendumSelection',
            fields=[
                ('ballotitemselection_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ballot.BallotItemSelection')),
                ('photo_url', models.ImageField(default=None, null=True, upload_to=b'', blank=True)),
                ('website_url', models.URLField(default=None, null=True, blank=True)),
                ('facebook_url', models.URLField(default=None, null=True, blank=True)),
                ('twitter_url', models.URLField(default=None, null=True, blank=True)),
                ('in_favor', models.NullBooleanField(default=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('ballot.ballotitemselection', models.Model),
        ),
        migrations.AddField(
            model_name='ballotitemselection',
            name='ballot_item',
            field=models.ForeignKey(to='ballot.BallotItem'),
        ),
        migrations.AddField(
            model_name='ballotitem',
            name='ballot',
            field=models.ForeignKey(related_name='ballot_items', to='ballot.Ballot'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='office_election',
            field=models.ForeignKey(to='ballot.OfficeElection'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='party',
            field=models.ForeignKey(default=None, blank=True, to='ballot.Party', null=True),
        ),
    ]
