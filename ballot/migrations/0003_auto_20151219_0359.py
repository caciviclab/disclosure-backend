# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ballot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contest',
            options={'verbose_name': 'race'},
        ),
        migrations.AlterModelOptions(
            name='locality',
            options={'verbose_name_plural': 'localities'},
        ),
        migrations.AlterModelOptions(
            name='referendum',
            options={'verbose_name': 'ballot measure'},
        ),
        migrations.AlterField(
            model_name='referendum',
            name='number',
            field=models.CharField(help_text=b"The referendum's number or letter.", max_length=5),
        ),
    ]
