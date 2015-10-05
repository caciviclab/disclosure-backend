# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command

def load_ballot_data(apps, schema_editor):
    call_command('loaddata', 'ballot_data', app='ballot')


class Migration(migrations.Migration):

    dependencies = [
        ('ballot', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_ballot_data),
    ]
