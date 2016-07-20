# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locality', '0002_locality_true_model_id'),
        ('finance', '0005_independentmoney_filing_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportingperiod',
            options={'ordering': ('locality', 'period_start', 'period_end', 'form')},
        ),
        migrations.AddField(
            model_name='reportingperiod',
            name='locality',
            field=models.ForeignKey(default=None, blank=True, to='locality.Locality', null=True),
        ),
    ]
