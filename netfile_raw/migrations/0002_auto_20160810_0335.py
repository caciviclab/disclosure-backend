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
            field=models.CharField(max_length=32, null=True, db_column='filerLocalId'),
        ),
        migrations.AddField(
            model_name='netfilecal201transaction',
            name='filerStateId',
            field=models.CharField(max_length=2, null=True, db_column='filerStateId'),
        ),
        migrations.AddField(
            model_name='netfilecal201transaction',
            name='filingEndDate',
            field=models.DateField(null=True, db_column='filingEndDate'),
        ),
        migrations.AddField(
            model_name='netfilecal201transaction',
            name='filingStartDate',
            field=models.DateField(null=True, db_column='filingStartDate'),
        ),
    ]
