from dal import autocomplete
from django import forms
from django.forms import Form
from django.utils.translation import gettext_lazy as _

from base.utils.api_utils import get_training_list_from_osis


class ProspectForm(Form):

    first_name = forms.CharField(
        required=True,
        label=_("First name")
    )

    name = forms.CharField(
        required=True,
        label=_("Name")
    )

    postal_code = forms.CharField(
        required=True,
        label=_("Postal code")
    )

    city = forms.CharField(
        required=True,
        label=_("City")
    )

    email = forms.EmailField(
        required=True,
        label=_("Email")
    )

    phone_number = forms.CharField(
        required=True,
        label=_("Phone number")
    )

    formation = autocomplete.Select2ListChoiceField(
        choice_list=get_training_list_from_osis,
        widget=autocomplete.ListSelect2(url='training-autocomplete'),
        required=True,
        label=_("Formation")
    )

    class Meta:
        fields = [
            'first_name',
            'last_name',
            'email',
            'gender'
        ]
