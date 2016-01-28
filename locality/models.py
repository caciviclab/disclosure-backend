from __future__ import unicode_literals
from django.db import models
from django.db.models.fields.related import OneToOneRel
from django.utils.encoding import python_2_unicode_compatible


class ReverseLookupStringMixin(object):
    def __str__(self):
        for relationship in self._meta.related_objects:
            attr = relationship.name
            if (isinstance(relationship, OneToOneRel) and hasattr(self, attr)):
                return unicode(getattr(self, attr))
        return ''


@python_2_unicode_compatible
class Locality(models.Model, ReverseLookupStringMixin):
    """
    A base table that gives a globally unique ID to any
    location (city, state, etc)
    """
    name = models.CharField(max_length=128, null=True, default=None)
    short_name = models.CharField(max_length=32, null=True, default=None)

    def __str__(self):
        return (ReverseLookupStringMixin.__str__(self) or
                self.name or self.short_name or str(self.id))

    class Meta:
        verbose_name_plural = 'localities'


class FipsMixin(Locality):
    """
    Abstract class, for any model that has a fips_id
    """
    fips_id = models.IntegerField(null=True, default=None)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class City(FipsMixin):
    """
    City
    """
    county = models.ForeignKey('County', null=True, default=None)
    state = models.ForeignKey('State')

    def __str__(self):
        return '%s, %s' % (self.name or self.short_name, self.state)

    class Meta:
        verbose_name_plural = 'cities'


@python_2_unicode_compatible
class County(FipsMixin):
    """
    County
    """
    state = models.ForeignKey('State')

    def __str__(self):
        # See https://code.djangoproject.com/ticket/25218 on why __unicode__
        return '%s, %s' % (Locality.__unicode__(self), self.state)

    class Meta:
        verbose_name_plural = 'counties'


@python_2_unicode_compatible
class State(FipsMixin):
    """
    State
    """
    def __str__(self):
        return self.short_name or self.name


@python_2_unicode_compatible
class ZipCode(Locality):
    """
    A Static set of ZIP code to "metro" name mappings.
    """
    city = models.ForeignKey('City', null=True, default=None)
    county = models.ForeignKey('County', null=True, default=None)
    state = models.ForeignKey('State', null=True, default=None)

    def __str__(self):
        return self.short_name or self.name


class AddressMixin(models.Model):
    """
    A street address.
    """
    street = models.CharField(max_length=1024, null=True, default=None)
    city = models.ForeignKey(
        'City', null=True, default=None,
        related_name='%(app_label)s_%(class)s_address_city')
    state = models.ForeignKey(
        'State', null=True, default=None,
        related_name='%(app_label)s_%(class)s_address_state')
    zip_code = models.ForeignKey(
        'ZipCode', null=True, default=None,
        related_name='%(app_label)s_%(class)s_address_zip_code')

    class Meta:
        abstract = True

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
