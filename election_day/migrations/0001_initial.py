# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ballot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectionDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ballot', models.ForeignKey(to='ballot.Ballot')),
            ],
        ),
    ]
