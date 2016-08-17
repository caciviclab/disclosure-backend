# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netfile_raw', '0002_auto_20160810_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='netfilecal201transaction',
            name='filerStateId',
            field=models.CharField(max_length=32, null=True, db_column='filerStateId'),
        ),
    ]
