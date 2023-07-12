from django.conf import settings
from django.core import checks
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string

from .core import Barcode

default_country = getattr(settings, 'BARCODE_COUNTRY', '950')
default_brand = getattr(settings, 'BARCODE_BRAND', '0000')


class BarcodeFieldDescriptor(object):
    """Field descriptor responsible for the seamless access of Barcode object properties"""

    def __init__(self, _name, _class):
        self._name = _name
        self._class = _class

    def __get__(self, instance=None, owner=None):
        value = instance.__dict__[self._name]
        if value is None:
            return value
        return self._class(value)

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value


class BarcodeField(models.CharField):
    """Barcode model field based on a EAN13 standard"""
    description = _('EAN13 Barcode.')

    def generate_default(self):
        return "".join([self.country, self.brand, get_random_string(5, '0123456789')])

    def contribute_to_class(self, cls, name):
        super(BarcodeField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, BarcodeFieldDescriptor(self.name, Barcode))

    def __init__(self, country: str = default_country, brand: str = default_brand, **kwargs):
        self.country = country
        self.brand = brand
        kwargs['max_length'] = 13
        kwargs['default'] = self.generate_default()
        super().__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        del kwargs['default']
        if self.country != default_country:
            kwargs['country'] = self.country
        if self.brand != default_brand:
            kwargs['brand'] = self.brand
        return name, path, args, kwargs

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_country(),
            *self._check_brand(),
        ]

    def _check_country(self):
        if len(self.country) != 3:
            return [
                checks.Error(
                    "%s's country argument must have a 3 digits." % self.__class__.__name__,
                    obj=self,
                    id='fields.E201',
                )
            ]
        else:
            return []

    def _check_brand(self):
        if len(self.brand) != 4:
            return [
                checks.Error(
                    "%s's country argument must have a 4 digits." % self.__class__.__name__,
                    obj=self,
                    id='fields.E201',
                )
            ]
        else:
            return []
