# -*- coding: utf-8 -*-
import os.path as op

from django.conf import settings
from django.core.management import call_command
from django.db import migrations


def load_ballot_data(apps, schema_editor):
    fixtures = (
        ('locality', op.join(settings.FIXTURES_DIR, '2016_03_27_locality.json')),
        ('ballot', op.join(settings.FIXTURES_DIR, '2016_03_27_ballot.json')),)

    for app, path in fixtures:
        call_command('loaddata', path, app=app)


class Migration(migrations.Migration):

    dependencies = [
        ('ballot', '0002_auto_20160304_2151'),
        ('locality', '0002_locality_true_model_id'),
    ]

    operations = [
        migrations.RunPython(load_ballot_data),
    ]
