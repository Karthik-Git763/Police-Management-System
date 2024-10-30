from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Witness, Evidence

class WitnessForm(forms.ModelForm):
    class Meta:
        model = Witness
        fields = ['first_name', 'last_name', 'statement', 'phone_number', 'gender', 'street', 'city', 'state']

class EvidenceForm(forms.ModelForm):
    class Meta:
        model = Evidence
        fields = ['name', 'crime', 'date', 'description', 'added_by']