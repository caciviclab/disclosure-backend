# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0009_auto_20160720_0725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='locality',
        ),
        migrations.DeleteModel(
            name='Form',
        ),
    ]
