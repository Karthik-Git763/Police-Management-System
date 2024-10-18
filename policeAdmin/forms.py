from django import forms
from django.contrib.auth.forms import UserCreationForm
from civilian.models import CustomUser
from police.models import PoliceModel,Station

from .models import AdminModel

class AddPoliceForm(UserCreationForm):# check later if working after admin login
    first_name=forms.CharField(max_length=50,required=True)
    last_name=forms.CharField(max_length=50,required=True)
    rank=forms.CharField(max_length=50,required=True)
    department=forms.CharField(max_length=50,required=True)
    phone_number=forms.CharField(max_length=50,required=True)
    status=forms.CharField(max_length=20,required=True,widget=forms.Select(choices=PoliceModel.status_choice))
    station=forms.ModelChoiceField(queryset=Station.objects.all())

    usable_password = None

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    class Meta:
        model=CustomUser
        fields=['username', 'email', 'password1', 'password2',"first_name","last_name","rank","department","phone_number","status","station"]
        labels={
            'first_name':'First Name',
            'last_name':"Last Name",
            'phone_number':"Phone Number"
        }
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.user_type = 'Police'
        if commit:
            user.save()
            admin_user=AdminModel.objects.get(user=self.request.user)
            station=self.cleaned_data["station"]
            noOfPolice=station.number_of_officers
            station.number_of_officers=noOfPolice+1
            station.save()

            police_model=PoliceModel(user=user,first_name=self.cleaned_data["first_name"],last_name=self.cleaned_data["last_name"],rank=self.cleaned_data["rank"],department=self.cleaned_data["department"],phone_number=self.cleaned_data["phone_number"],status=self.cleaned_data["status"],station=self.cleaned_data["station"],add_by=admin_user)
            police_model.save()
        return user 
    
class AddStationForm(forms.ModelForm):
    class Meta:
        model=Station
        fields=["location","phone_number"]
        labels={
            "location":"Location",
            "phone_number":"Phone Number"
        }


class AddPoliceAdminForm(UserCreationForm):# check later if working after admin login
    first_name=forms.CharField(max_length=50,required=True)
    last_name=forms.CharField(max_length=50,required=True)
    phone_number=forms.CharField(max_length=50,required=True)


    usable_password = None    

    class Meta:
        model=CustomUser
        fields=['username', 'email', 'password1', 'password2',"first_name","last_name","phone_number"]
        labels={
            'first_name':"First Name",
            'last_name':"Last Name",
            'phone_number':"Phone Number"
        }
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.user_type = 'Admin'
        user.is_staff=True
        user.is_superuser=True
        if commit:
            user.save()
            police_model=AdminModel(user=user,first_name=self.cleaned_data["first_name"],last_name=self.cleaned_data["last_name"],phone_number=self.cleaned_data["phone_number"])
            police_model.save()
        return user

