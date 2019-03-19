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
from django.http import Http404

from base.models.person import Person
from base.views.common import access_denied
from continuing_education.views.api import get_admission, get_registration


def has_participant_access(view_func):
    def f_has_participant_access(request, admission_uuid=None):
        if admission_uuid:
            person_uuid = str(Person.objects.get(user=request.user).uuid)
            try:
                admission = get_admission(admission_uuid)
            except Http404:
                admission = get_registration(admission_uuid)
            if admission.get('uuid') and admission['person_information']['person']['uuid'] != person_uuid:
                return access_denied(request)
        return view_func(request, admission_uuid)

    return f_has_participant_access
