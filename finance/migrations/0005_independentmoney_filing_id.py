# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='independentmoney',
            name='filing_id',
            field=models.CharField(default=None, max_length=32, null=True, help_text='Transaction ID (specific to government processing entity)', blank=True),
        ),
    ]
