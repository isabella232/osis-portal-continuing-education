from django.db import models
from django.utils.translation import ugettext_lazy as _

from osis_common.models.serializable_model import SerializableModelAdmin, SerializableModel


class AddressAdmin(SerializableModelAdmin):
    list_display = ('location', 'postal_code', 'city', 'country')


class Address(SerializableModel):
    location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("location")
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("postal_code")
    )
    city = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("city")
    )
    country = models.ForeignKey(
        'reference.Country',
        blank=True,
        null=True,
        related_name='address_country',
        verbose_name=_("country")
    )
