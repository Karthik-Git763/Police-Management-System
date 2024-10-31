from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import widgets



class WitnessForm(forms.ModelForm):
    class Meta:
        model = Witness
        fields = [
            "first_name",
            "last_name",
            "statement",
            "phone_number",
            "gender",
            "street",
            "city",
            "state",
        ]


class EvidenceForm(forms.ModelForm):
    class Meta:
        model = Evidence
        fields = ['name', 'date', 'description']

class SuspectForm(forms.ModelForm):
    class Meta:
        model = Suspect
        fields = ['first_name', 'last_name', 'phone_number', 'gender', 'date_of_birth', 'street', 'city', 'state']

class VictimForm(forms.ModelForm):
    class Meta:
        model = Victim
        fields = ['first_name', 'last_name', 'phone_number', 'gender', 'date_of_birth', 'street', 'city', 'state']
        fields = ["name", "crime", "date", "description", "added_by"]


class CriminalForm(forms.ModelForm):
    class Meta:
        model = Criminal
        fields = [
            "first_name",
            "last_name",
            "street",
            "city",
            "state",
            "status",
            "gender",
            "date_of_birth",
            "crime",
        ]

        widgets = {"crime": forms.SelectMultiple(attrs={"class": "select2"})}
