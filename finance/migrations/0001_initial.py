# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import locality.models


class Migration(migrations.Migration):

    dependencies = [
        ('locality', '0001_initial'),
        ('ballot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefactor',
            fields=[
                ('benefactor_id', models.AutoField(serialize=False, primary_key=True)),
                ('benefactor_type', models.CharField(max_length=2, choices=[('PF', 'Primarily-formed committee'), ('IF', 'Independently-formed committee'), ('IN', 'Individual'), ('PY', 'Political Party'), ('OT', 'Other')])),
            ],
            options={
                'ordering': ('benefactor_locality__name', 'benefactor_locality__short_name'),
            },
            bases=(models.Model, locality.models.ReverseLookupStringMixin),
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(default=None, max_length=1024, null=True, blank=True)),
                ('photo_url', models.ImageField(default=None, null=True, upload_to=b'', blank=True)),
                ('website_url', models.URLField(default=None, null=True, blank=True)),
                ('facebook_url', models.URLField(default=None, null=True, blank=True)),
                ('twitter_url', models.URLField(default=None, null=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('filer_id', models.CharField(default=None, max_length=16, null=True, help_text='Official government ID (none if unknown)')),
                ('type', models.CharField(max_length=2, choices=[('CC', 'Candidate Controlled Committee'), ('PF', 'Primarily Formed Committees'), ('IC', 'General Purpose Committees'), ('BM', 'Ballot Measure Committee')])),
            ],
            options={
                'ordering': ('name', 'locality__name', 'locality__short_name'),
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('text_id', models.CharField(help_text='e.g. 460 Schedule A', max_length=32)),
                ('submission_frequency', models.CharField(max_length=2, choices=[('24', '24 hours'), ('SA', 'Semi-annual'), ('QU', 'Quarterly'), ('OT', 'Other')])),
                ('locality', models.ForeignKey(default=None, blank=True, to='locality.Locality', help_text='Only set when a form is specific to a locality.', null=True)),
            ],
            options={
                'ordering': ('locality__name', 'locality__short_name', 'name'),
            },
        ),
        migrations.CreateModel(
            name='IndependentMoney',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField(help_text='Monetary value of the benefit.')),
                ('cumulative_amount', models.FloatField(help_text='Total monetary value of provided benefits, to date of this transaction.')),
                ('report_date', models.DateField()),
                ('source', models.CharField(help_text='e.g. Netfile', max_length=2, choices=[('NF', 'Netfile')])),
                ('source_xact_id', models.CharField(help_text='Transaction ID (specific to data source)', max_length=32)),
            ],
            options={
                'ordering': ('-reporting_period__period_start', '-reporting_period__period_end', '-beneficiary__ballot_item_selection__ballot_item__ballot__date', '-report_date'),
                'verbose_name_plural': 'independent money',
            },
        ),
        migrations.CreateModel(
            name='ReportingPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period_start', models.DateField()),
                ('period_end', models.DateField()),
                ('form', models.ForeignKey(to='finance.Form')),
            ],
            options={
                'ordering': ('period_start', 'period_end'),
            },
        ),
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('committee_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='finance.Committee')),
                ('support', models.NullBooleanField(default=None, help_text='Whether funds are to support (Y) or oppose (N)')),
                ('ballot_item_selection', models.ForeignKey(default=None, to='ballot.BallotItemSelection', null=True)),
            ],
            options={
                'ordering': ('name', 'locality__name', 'locality__short_name'),
                'verbose_name_plural': 'beneficiaries',
            },
            bases=('finance.committee',),
        ),
        migrations.CreateModel(
            name='CommitteeBenefactor',
            fields=[
                ('committee_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='finance.Committee')),
                ('benefactor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='finance.Benefactor')),
            ],
            options={
                'ordering': ('benefactor_locality__name', 'benefactor_locality__short_name', 'name', 'locality__name', 'locality__short_name'),
            },
            bases=('finance.benefactor', 'finance.committee'),
        ),
        migrations.CreateModel(
            name='OtherBenefactor',
            fields=[
                ('benefactor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='finance.Benefactor')),
                ('street', models.CharField(default=None, max_length=1024, null=True, blank=True)),
                ('photo_url', models.ImageField(default=None, null=True, upload_to=b'', blank=True)),
                ('website_url', models.URLField(default=None, null=True, blank=True)),
                ('facebook_url', models.URLField(default=None, null=True, blank=True)),
                ('twitter_url', models.URLField(default=None, null=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('city', models.ForeignKey(related_name='finance_otherbenefactor_address_city', default=None, blank=True, to='locality.City', null=True)),
                ('locality', models.ForeignKey(default=None, blank=True, to='locality.Locality', null=True)),
                ('state', models.ForeignKey(related_name='finance_otherbenefactor_address_state', default=None, blank=True, to='locality.State', null=True)),
                ('zip_code', models.ForeignKey(related_name='finance_otherbenefactor_address_zip_code', default=None, blank=True, to='locality.ZipCode', null=True)),
            ],
            options={
                'ordering': ('benefactor_locality__name', 'benefactor_locality__short_name', 'name', 'locality__name', 'locality__short_name'),
            },
            bases=('finance.benefactor', models.Model),
        ),
        migrations.CreateModel(
            name='PartyBenefactor',
            fields=[
                ('benefactor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='finance.Benefactor')),
                ('name', models.CharField(max_length=256)),
                ('party', models.ForeignKey(to='ballot.Party')),
            ],
            options={
                'ordering': ('name', 'party__name', 'benefactor_locality__name', 'benefactor_locality__short_name'),
            },
            bases=('finance.benefactor',),
        ),
        migrations.CreateModel(
            name='PersonBenefactor',
            fields=[
                ('benefactor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='finance.Benefactor')),
                ('street', models.CharField(default=None, max_length=1024, null=True, blank=True)),
                ('photo_url', models.ImageField(default=None, null=True, upload_to=b'', blank=True)),
                ('website_url', models.URLField(default=None, null=True, blank=True)),
                ('facebook_url', models.URLField(default=None, null=True, blank=True)),
                ('twitter_url', models.URLField(default=None, null=True, blank=True)),
                ('first_name', models.CharField(default=None, max_length=255, null=True, help_text="The person's first name.")),
                ('middle_name', models.CharField(default=None, max_length=255, null=True, help_text="The person's middle name.", blank=True)),
                ('last_name', models.CharField(help_text="The person's last name.", max_length=255)),
                ('occupation', models.CharField(max_length=64, null=True)),
                ('city', models.ForeignKey(related_name='finance_personbenefactor_address_city', default=None, blank=True, to='locality.City', null=True)),
                ('state', models.ForeignKey(related_name='finance_personbenefactor_address_state', default=None, blank=True, to='locality.State', null=True)),
                ('zip_code', models.ForeignKey(related_name='finance_personbenefactor_address_zip_code', default=None, blank=True, to='locality.ZipCode', null=True)),
            ],
            options={
                'ordering': ('benefactor_locality__name', 'benefactor_locality__short_name', 'last_name', 'first_name', 'middle_name'),
            },
            bases=('finance.benefactor', models.Model),
        ),
        migrations.AddField(
            model_name='independentmoney',
            name='benefactor',
            field=models.ForeignKey(help_text='Gave the benefit', to='finance.Benefactor'),
        ),
        migrations.AddField(
            model_name='independentmoney',
            name='benefactor_zip',
            field=models.ForeignKey(to='locality.ZipCode'),
        ),
        migrations.AddField(
            model_name='independentmoney',
            name='reporting_period',
            field=models.ForeignKey(to='finance.ReportingPeriod'),
        ),
        migrations.AddField(
            model_name='committee',
            name='city',
            field=models.ForeignKey(related_name='finance_committee_address_city', default=None, blank=True, to='locality.City', null=True),
        ),
        migrations.AddField(
            model_name='committee',
            name='locality',
            field=models.ForeignKey(default=None, blank=True, to='locality.Locality', null=True),
        ),
        migrations.AddField(
            model_name='committee',
            name='state',
            field=models.ForeignKey(related_name='finance_committee_address_state', default=None, blank=True, to='locality.State', null=True),
        ),
        migrations.AddField(
            model_name='committee',
            name='zip_code',
            field=models.ForeignKey(related_name='finance_committee_address_zip_code', default=None, blank=True, to='locality.ZipCode', null=True),
        ),
        migrations.AddField(
            model_name='benefactor',
            name='benefactor_locality',
            field=models.ForeignKey(default=None, blank=True, to='locality.Locality', null=True),
        ),
        migrations.AddField(
            model_name='independentmoney',
            name='beneficiary',
            field=models.ForeignKey(help_text='Got the benefit', to='finance.Beneficiary'),
        ),
    ]
