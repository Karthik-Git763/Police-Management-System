from django import forms
from django.contrib.auth.forms import UserCreationForm
from civilian.models import CustomUser
from police.models import PoliceModel,Station
from .models import AdminModel

class AddPolice(UserCreationForm):
    first_name=forms.CharField(max_length=50,required=True)
    last_name=forms.CharField(max_length=50,required=True)
    rank=forms.CharField(max_length=50,required=True)
    department=forms.CharField(max_length=50,required=True)
    phone_number=forms.CharField(max_length=50,required=True)
    status=forms.CharField(max_length=20,required=True,widget=forms.Select(choices=PoliceModel.status_choice))
    station=forms.ModelChoiceField(queryset=Station.objects.all())

    class Meta:
        model=CustomUser
        fields=['username', 'email', 'password1', 'password2',"first_name","last_name","rank","department","phone_number","status","station"]
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.user_type = 'Police'
        if commit:
            user.save()
            admin_user=AdminModel.objects.get(user=self.request.user)
            police_model=PoliceModel(user=user,first_name=self.cleaned_data["first_name"],last_name=self.cleaned_data["last_name"],rank=self.cleaned_data["rank"],department=self.cleaned_data["department"],phone_number=self.cleaned_data["phone_number"],status=self.cleaned_data["status"],station=self.cleaned_data["station"],add_by=admin_user)
            police_model.save()
        return user
    