# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ballot', '0003_auto_20151219_0359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='contest_type',
            field=models.CharField(help_text=b'Office if the contest is for a person, referendum if the contest is for an issue.', max_length=1, choices=[(b'R', b'Referendum'), (b'O', b'Office')]),
        ),
    ]
