# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_auto_20160320_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportingperiod',
            name='filing_deadline',
            field=models.DateField(default=None, null=True, blank=True),
        ),
    ]
