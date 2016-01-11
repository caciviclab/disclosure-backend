from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Locality(models.Model):
    """
    A base table that gives a globally unique ID to any
    location (city, state, etc)
    """
    name = models.CharField(max_length=128, null=True, default=None)
    short_name = models.CharField(max_length=32, null=True, default=None)

    def __str__(self):
        return self.name or self.short_name or str(self.id)

    class Meta:
        verbose_name_plural = 'localities'


class FipsMixin(Locality):
    """
    Abstract class, for any model that has a fips_id
    """
    fips_id = models.IntegerField(null=True, default=None)

    class Meta:
        abstract = True


class City(FipsMixin):
    """
    City
    """
    county = models.ForeignKey('County', null=True, default=None)
    state = models.ForeignKey('State')

    class Meta:
        verbose_name_plural = 'cities'


class County(FipsMixin):
    """
    County
    """
    state = models.ForeignKey('State')

    class Meta:
        verbose_name_plural = 'counties'


class State(FipsMixin):
    """
    State
    """
    pass


class ZipCode(Locality):
    """
    A Static set of ZIP code to "metro" name mappings.
    """
    city = models.ForeignKey('City', null=True, default=None)
    county = models.ForeignKey('County', null=True, default=None)
    state = models.ForeignKey('State', null=True, default=None)


@python_2_unicode_compatible
class Address(models.Model):
    """
    A street address.
    """
    street = models.CharField(max_length=1024, null=True, default=None)
    city = models.ForeignKey('City', null=True, default=None)
    county = models.ForeignKey('County', null=True, default=None)
    state = models.ForeignKey('State', null=True, default=None)
    zip_code = models.ForeignKey('ZipCode', null=True, default=None)

    def __str__(self):
        return '%s, %s, %s %s' % (
            self.street, self.city, self.state, self.zip_code)

    class Meta:
        verbose_name_plural = 'addresses'


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
