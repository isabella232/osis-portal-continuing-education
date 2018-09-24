##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2017 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.test import TestCase

from continuing_education.forms.admission import AdmissionForm
from continuing_education.tests.factories.admission import AdmissionFactory
from reference.models import country


class TestAdmissionForm(TestCase):

    def test_valid_form(self):
        admission = AdmissionFactory()
        form = AdmissionForm(admission.__dict__)
        self.assertTrue(form.is_valid(), form.errors)

def convert_countries(person):
    person['birth_country'] = country.Country.objects.get(pk=person["birth_country_id"])
    person['citizenship'] = country.Country.objects.get(pk=person["citizenship_id"])

def convert_dates(person):
    person['high_school_graduation_year'] = person['high_school_graduation_year'].strftime('%Y-%m-%d')
    person['last_degree_graduation_year'] = person['last_degree_graduation_year'].strftime('%Y-%m-%d')
