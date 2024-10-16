from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, CivilianModel

class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=50, required=True)
    date_of_birth = forms.DateField(required=True)
    city = forms.CharField(max_length=50, required=True)
    street = forms.CharField(max_length=50, required=True)
    state = forms.CharField(max_length=50, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'name', 'date_of_birth', 'city', 'street', 'state']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'Civilian'
        if commit:
            user.save()
            civilian_model=CivilianModel(name = self.cleaned_data['name'], date_of_birth = self.cleaned_data['date_of_birth'], city = self.cleaned_data['city'], street = self.cleaned_data['street'], state = self.cleaned_data['state'], user=user)
            civilian_model.save()

        return user