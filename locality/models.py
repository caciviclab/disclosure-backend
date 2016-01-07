from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Locality(models.Model):
    """
    A base table that gives a globally unique ID to any
    location (city, state, etc)
    """
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=32)

    def __str__(self):
        return self.name or self.short_name or str(self.id)

    def dereference(self):
        for rel in self._meta.get_all_related_objects():
            if hasattr(self, rel.name):
                return getattr(self, rel.name)
        raise Exception("Abstract locality? %s" % self)

    class Meta:
        verbose_name_plural = 'localities'


class FipsLocality(Locality):
    """
    Abstract class, for any model that has a fips_id
    """
    fips_id = models.IntegerField(null=True)

    class Meta:
        abstract = True


class City(FipsLocality):
    """
    City
    """
    county = models.ForeignKey('County', null=True)
    state = models.ForeignKey('State')


class County(FipsLocality):
    """
    County
    """
    state = models.ForeignKey('State')


class State(FipsLocality):
    """
    State
    """
    pass


class ZipCode(Locality):
    """
    A Static set of ZIP code to "metro" name mappings.
    """
    city = models.ForeignKey('City', null=True)
    county = models.ForeignKey('County', null=True)
    state = models.ForeignKey('State', null=True)


@python_2_unicode_compatible
class Address(models.Model):
    street = models.CharField(max_length=1024, null=True)
    city = models.ForeignKey('City', null=True)
    county = models.ForeignKey('County', null=True)
    state = models.ForeignKey('State', null=True)
    zip_code = models.ForeignKey('ZipCode', null=True)

    def __str__(self):
        return '%s, %s, %s %s' % (
            self.street, self.city, self.state, self.zip_code)


'''
class Precinct(Locality):
    """
    The smallest unit of geographic area for voters. Your precinct determines
    who and what you vote on.
    """
    number = models.CharField(
        max_length=5,
        help_text="the precinct's number e.g., 32 or 32A "
                  "(alpha characters are legal)."
    )
    zip_code = models.ForeignKey('ZipCode')


@python_2_unicode_compatible
class PSA(Locality):
    """
    """
    code = models.IntegerField()
    title = models.CharField(
        max_length=1024,
    )
    city = models.ForeignKey('City', null=True)
    county = models.ForeignKey('County', null=True)
    state = models.ForeignKey('State', null=True)
    zip_code = models.ForeignKey('ZipCode', null=True)

    def __str__(self):
        return "%d: %s" % (self.zip_code, self.city.name)
'''
