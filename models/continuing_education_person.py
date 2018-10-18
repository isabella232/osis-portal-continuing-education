from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from osis_common.models.serializable_model import SerializableModelAdmin, SerializableModel


class ContinuingEducationPersonAdmin(SerializableModelAdmin):
    list_display = ('person', 'birth_date',)
    search_fields = ['first_name', 'last_name']
    list_filter = ('birth_country',)


class ContinuingEducationPerson(SerializableModel):
    person = models.OneToOneField(
        'base.Person',
        on_delete=models.CASCADE
    )

    birth_date = models.DateField(
        blank=True,
        default=datetime.now,
        verbose_name=_("birth_date")
    )

    birth_location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("birth_location")
    )
    birth_country = models.ForeignKey(
        'reference.Country',
        blank=True,
        null=True,
        related_name='birth_country',
        verbose_name=_("birth_country")
    )

    def __str__(self):
        return "{} - {} {}".format(self.id, self.person.first_name, self.person.last_name)


def find_by_person(person):
    return ContinuingEducationPerson.objects.filter(person=person).first()
