# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ballot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='office_election',
            field=models.ForeignKey(related_name='candidates', to='ballot.OfficeElection'),
        ),
    ]
