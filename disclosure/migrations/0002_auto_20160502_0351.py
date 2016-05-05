# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path as op

from django.conf import settings
from django.core.management import call_command
from django.db import migrations


def load_ballot_data(apps, schema_editor):
    fixtures = (
        ('ballot', op.join(settings.FIXTURES_DIR, '2016_05_01_ballot.json')),)

    for app, path in fixtures:
        call_command('loaddata', path, app=app)


class Migration(migrations.Migration):

    dependencies = [
        ('disclosure', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_ballot_data),
    ]
