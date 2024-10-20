from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Witness

class WitnessForm(forms.ModelForm):
    class Meta:
        model = Witness
        fields = ['first_name', 'last_name', 'statement', 'phone_number', 'gender', 'street', 'city', 'state']
