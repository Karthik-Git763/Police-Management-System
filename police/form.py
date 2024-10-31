from django import forms
from django.forms import widgets

# from django.contrib.auth.forms import UserCreationForm
# from django.db.models.expressions import fields
from .models import Witness, Evidence, Criminal


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
