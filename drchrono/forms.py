from django import forms
from django.forms import widgets

from localflavor.us.forms import (
    USSocialSecurityNumberField,
    USStateField,
    USStateSelect,
)

from drchrono.models import Patient


class PatientSignInForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)


class PatientDemographicsForm(forms.ModelForm):
    state = USStateField(widget=USStateSelect)

    class Meta:
        model = Patient
        fields = ["first_name", "last_name", "address", "city", "state", "zip_code", "email"]
