# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0007_reportingperiod_filing_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='text_id',
            field=models.CharField(help_text='e.g. 460A', max_length=32),
        ),
    ]
