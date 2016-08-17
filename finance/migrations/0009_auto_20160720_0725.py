# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0008_auto_20160320_2349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportingperiod',
            name='form',
        ),
        migrations.RemoveField(
            model_name='reportingperiod',
            name='locality',
        ),
        migrations.AlterModelOptions(
            name='independentmoney',
            options={'ordering': ('-beneficiary__ballot_item_selection__ballot_item__ballot__date', '-report_date'), 'verbose_name_plural': 'independent money'},
        ),
        migrations.RemoveField(
            model_name='independentmoney',
            name='reporting_period',
        ),
        migrations.DeleteModel(
            name='ReportingPeriod',
        ),
    ]
