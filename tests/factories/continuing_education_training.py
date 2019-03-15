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
import uuid

import factory

from base.tests.factories.education_group import EducationGroupFactory
from base.tests.factories.education_group_year import EducationGroupYearFactory
from continuing_education.models.continuing_education_training import ContinuingEducationTraining


def ContinuingEducationTrainingDictFactory(active=True):
    ed = EducationGroupFactory()
    edy = EducationGroupYearFactory(education_group=ed)
    cet = {
        'uuid': uuid.uuid4(),
        'active': active,
        'education_group': {
            'uuid': ed.uuid,
            'acronym': edy.acronym
        },
    }
    return cet


class ContinuingEducationTrainingFactory(factory.DjangoModelFactory):
    class Meta:
        model = ContinuingEducationTraining

    active = True
    education_group = factory.SubFactory(EducationGroupFactory)
