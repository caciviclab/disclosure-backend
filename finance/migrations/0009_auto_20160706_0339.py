# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path as op

from django.conf import settings
from django.core.management import call_command
from django.db import models, migrations


def load_ballot_data(apps, schema_editor):
    fixtures = (
        ('finance', op.join(settings.FIXTURES_DIR, '2016_07_05_form.json')),
        ('finance', op.join(settings.FIXTURES_DIR, '2016_07_05_reporting_period.json')),
    )

    for app, path in fixtures:
        call_command('loaddata', path, app=app)


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0008_auto_20160320_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportingperiod',
            name='permanent',
            field=models.BooleanField(default=True, help_text='Whether data is reported once, or re-reported.'),
        ),
        migrations.RunPython(load_ballot_data),
    ]
