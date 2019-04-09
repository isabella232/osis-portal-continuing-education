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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from unittest import mock

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from rest_framework import status

from base.tests.factories.academic_year import create_current_academic_year, AcademicYearFactory
from base.tests.factories.person import PersonFactory
from continuing_education.models.enums.admission_state_choices import SUBMITTED
from continuing_education.tests.factories.admission import AdmissionDictFactory
from continuing_education.tests.factories.continuing_education_training import ContinuingEducationTrainingDictFactory
from continuing_education.tests.factories.person import ContinuingEducationPersonDictFactory
from continuing_education.views.api import get_token_from_osis, get_personal_token


class ApiMethodsTestCase(TestCase):
    def setUp(self):
        current_acad_year = create_current_academic_year()
        self.next_acad_year = AcademicYearFactory(year=current_acad_year.year + 1)
        self.user = User.objects.create_user('demo', 'demo@demo.org', 'passtest')
        self.client.force_login(self.user)
        self.request = RequestFactory()
        self.request.session = {}
        self.request.user = self.user
        self.person = PersonFactory(user=self.user)
        self.person_information = ContinuingEducationPersonDictFactory(self.person.uuid)
        self.formation = ContinuingEducationTrainingDictFactory()
        self.admission = AdmissionDictFactory(self.person_information)

        self.admission_submitted = AdmissionDictFactory(self.person_information, SUBMITTED)

    @mock.patch('requests.post', return_value=HttpResponse(content=b'{"token": "token"}', status=status.HTTP_200_OK))
    def test_get_token_from_osis(self, mock_post):
        token = get_token_from_osis(self.user.username)
        self.assertEqual(token, "token")

    @mock.patch('requests.post', return_value=HttpResponse(status=status.HTTP_404_NOT_FOUND))
    def test_get_token_from_osis_not_found(self, mock_post):
        token = get_token_from_osis(self.user.username)
        self.assertEqual(token, "")

    @mock.patch('requests.post', return_value=HttpResponse(content=b'{"token": "token"}', status=status.HTTP_200_OK))
    def test_get_personal_token_not_in_session(self, mock_post):
        token = get_personal_token(self.request)
        self.assertEqual(token, "token")
        self.assertEqual(self.request.session['personal_token'], "token")
        mock_post.assert_called()

    @mock.patch('requests.post')
    def test_get_personal_token_in_session(self, mock_post):
        self.request.session['personal_token'] = 'token'
        token = get_personal_token(self.request)
        self.assertEqual(token, "token")
        self.assertEqual(self.request.session['personal_token'], "token")
        self.assertFalse(mock_post.called)
