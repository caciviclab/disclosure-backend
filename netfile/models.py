from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_raw.models.base import CalAccessBaseModel

@python_2_unicode_compatible
class NetFileAgency(CalAccessBaseModel):
    """
    Netfile "Agencies" for reporting data.
    """
    agency_id = models.IntegerField(
        db_column='id',
        primary_key = True,
    )
    shortcut_name = models.CharField(
        max_length=1024,
        db_column='shortcut'
    )
    name = models.CharField(
        max_length=1024,
        db_column='name'
    )

    class Meta:
        app_label = 'netfile'
        db_table = 'netfile_agency'
        verbose_name = 'NETFILE_AGENCY'
        verbose_name_plural = 'NETFILE_AGENCY'

    def __str__(self):
        return "%: %s" % (self.agency_id, self.name)

