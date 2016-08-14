# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netfile_raw', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='netfilecal201transaction',
            name='filerLocalId',
            field=models.CharField(default='Unknown', max_length=32, db_column='filerLocalId'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='netfilecal201transaction',
            name='filerStateId',
            field=models.CharField(default='Unknown', max_length=32, db_column='filerStateId'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='netfilecal201transaction',
            name='filingEndDate',
            field=models.DateField(default='1970-01-01', db_column='filingEndDate'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='netfilecal201transaction',
            name='filingStartDate',
            field=models.DateField(default='1970-01-01', db_column='filingStartDate'),
            preserve_default=False,
        ),
    ]
