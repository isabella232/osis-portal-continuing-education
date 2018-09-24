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
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from continuing_education.forms.account import ContinuingEducationPersonForm
from continuing_education.forms.address import AddressForm
from continuing_education.forms.admission import AdmissionForm
from continuing_education.forms.person import PersonForm
from continuing_education.models.address import Address
from continuing_education.models.admission import Admission
from continuing_education.models.continuing_education_person import ContinuingEducationPerson
from continuing_education.views.common import display_errors

@login_required
def admission_detail(request, admission_id):
    admission = get_object_or_404(Admission, pk=admission_id)
    return render(request, "admission_detail.html", locals())

@login_required
def admission_new(request):
    person = get_object_or_404(ContinuingEducationPerson, pk=request.GET['person_information']) if 'person_information' in request.GET else None
    address = person.address if person else None
    admission_form = AdmissionForm(request.POST or None)
    person_form = ContinuingEducationPersonForm(request.POST or None, instance=person)
    address_form = AddressForm(request.POST or None, instance=address)
    errors = []
    if admission_form.is_valid() and person_form.is_valid() and address_form.is_valid():
        address = address_form.save()
        person = person_form.save(commit=False)
        person.address = address
        person.save()
        admission = admission_form.save(commit=False)
        admission.person = person
        admission.save()
        return redirect(reverse('continuing_education_home'))
    else:
        errors.append(admission_form.errors)
        errors.append(person_form.errors)
        errors.append(address_form.errors)
        display_errors(request, errors)

    return render(request, 'admission_form.html', locals())

@login_required
def admission_edit(request, admission_id):
    admission = get_object_or_404(Admission, pk=admission_id)
    person = get_object_or_404(ContinuingEducationPerson, pk=request.GET['person']) if 'person' in request.GET else admission.person
    admission_form = AdmissionForm(request.POST or None, instance=admission)
    person_form = PersonForm(request.POST or None, instance=person)
    address_form = AddressForm(request.POST or None, instance=person.address)
    errors = []
    if admission_form.is_valid() and person_form.is_valid() and address_form.is_valid():
        address, created = Address.objects.get_or_create(**address_form.cleaned_data)
        person = person_form.save(commit=False)
        person.address = address
        person.save()
        admission = admission_form.save(commit=False)
        admission.person = person
        admission.save()
        return redirect(reverse('admission_detail', kwargs={'admission_id':admission_id}))
    else:
        errors.append(admission_form.errors)
        errors.append(person_form.errors)
        errors.append(address_form.errors)
        display_errors(request, errors)

    return render(request, 'admission_form.html', locals())