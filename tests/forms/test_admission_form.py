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
import random

from django.forms import model_to_dict
from django.test import TestCase

from base.tests.factories.academic_year import create_current_academic_year, AcademicYearFactory
from base.tests.factories.education_group import EducationGroupFactory
from base.tests.factories.education_group_year import EducationGroupYearFactory
from continuing_education.forms.admission import AdmissionForm
from continuing_education.models.enums.admission_state_choices import ADMIN_STATE_CHOICES
from continuing_education.models.enums.enums import get_enum_keys
from continuing_education.tests.factories.admission import AdmissionFactory
from continuing_education.tests.factories.continuing_education_training import ContinuingEducationTrainingFactory
from reference.models import country


class TestAdmissionForm(TestCase):
    def setUp(self):
        current_acad_year = create_current_academic_year()
        self.next_acad_year = AcademicYearFactory(year=current_acad_year.year + 1)
        education_group = EducationGroupFactory()
        EducationGroupYearFactory(
            education_group=education_group,
            academic_year=current_acad_year
        )
        self.formation = ContinuingEducationTrainingFactory(
            education_group=education_group,
            active=True
        )

    def test_valid_form(self):
        admission = AdmissionFactory(
            formation=self.formation
        )
        data = model_to_dict(admission)
        form = AdmissionForm(data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_student_state(self):
        admission = AdmissionFactory(
            formation=self.formation,
            state=random.choice(get_enum_keys(ADMIN_STATE_CHOICES))
        )
        data = model_to_dict(admission)
        form = AdmissionForm(data)
        self.assertFalse(form.is_valid(), form.errors)


def convert_countries(person):
    person['birth_country'] = country.Country.objects.get(pk=person["birth_country_id"])
    person['citizenship'] = country.Country.objects.get(pk=person["citizenship_id"])


def convert_dates(person):
    person['high_school_graduation_year'] = person['high_school_graduation_year'].strftime('%Y-%m-%d')
    person['last_degree_graduation_year'] = person['last_degree_graduation_year'].strftime('%Y-%m-%d')
