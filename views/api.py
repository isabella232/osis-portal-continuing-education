##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2018 Université catholique de Louvain (http://www.uclouvain.be)
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
import io

import requests
from django.conf import settings
from rest_framework.parsers import JSONParser
from rest_framework.renderers import MultiPartRenderer

from base.views.autocomplete.common import get_list_from_osis


def transform_response_to_data(response):
    stream = io.BytesIO(response.content)
    data = JSONParser().parse(stream)
    if 'results' in data:
        data = data['results']
    return data


def get_data_list_from_osis(object_name, filter_field=None, filter_value=None):
    header_to_get = {'Authorization': 'Token ' + settings.OSIS_PORTAL_TOKEN}
    url = settings.URL_CONTINUING_EDUCATION_FILE_API + object_name + "/"
    if filter_field and filter_value:
        url = url + "?" + filter_field + "=" + filter_value
    response = requests.get(
        url=url,
        headers=header_to_get
    )
    return transform_response_to_data(response)


def get_data_from_osis(object_name, uuid):
    header_to_get = {'Authorization': 'Token ' + settings.OSIS_PORTAL_TOKEN}
    url = settings.URL_CONTINUING_EDUCATION_FILE_API + object_name + "/" + str(uuid)
    response = requests.get(
        url=url,
        headers=header_to_get
    )
    return transform_response_to_data(response)


def _prepare_headers_for_files(method):
    if method in ['GET', 'DELETE']:
        return {'Authorization': 'Token ' + settings.OSIS_PORTAL_TOKEN}
    elif method == 'POST':
        return {
            'Authorization': 'Token ' + settings.OSIS_PORTAL_TOKEN,
            'Content-Disposition': 'attachment; filename=name.jpeg',
            'Content-Type': MultiPartRenderer.media_type
        }


def get_country_list_from_osis():
    return get_list_from_osis(settings.URL_COUNTRY_API)


def get_training_list_from_osis():
    return get_list_from_osis(settings.URL_TRAINING_API)
