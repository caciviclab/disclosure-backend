# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locality', '0002_locality_true_model_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='fips_id',
        ),
        migrations.RemoveField(
            model_name='county',
            name='fips_id',
        ),
        migrations.RemoveField(
            model_name='state',
            name='fips_id',
        ),
    ]
