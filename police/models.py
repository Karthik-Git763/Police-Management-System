from django.db import models
from django.utils import timezone
from ..civilian.models import CustomUser
from ..policeAdmin.models import AdminModel
# Create your models here.

class Station(models.Model):
    location=models.CharField(max_length=100)
    number_of_officers=models.PositiveIntegerField(default=0)
    phone_number=models.CharField(max_length=15)
    def __str__(self):
        return self.location


class Crime(models.Model):
    statusChoice=[("Completed","Completed"),("Investigating","Investigating"),("Request Pending","Request Pending")]
    
    crime_type=models.CharField(max_length=50)
    description=models.TextField()
    location=models.CharField(max_length=50)
    status=models.CharField( max_length=50,choices=statusChoice)

class PoliceModel(models.Model):
    status_choice=[("On Duty","On Duty"),("Free","Free"),("Not Working","Not Working")]
    
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    rank=models.CharField(max_length=20)
    department=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=15)
    status=models.CharField( max_length=50,choices=status_choice)
    station=models.ForeignKey(Station,on_delete=models.CASCADE)
    current_crime=models.ForeignKey(Crime,on_delete=models.CASCADE)
    add_by=models.ForeignKey(AdminModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Witness(models.Model):
    genderChoice=[("M","Male"),("F","Females")]

    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    statement=models.TextField()
    phone_number=models.CharField(max_length=15)
    gender=models.CharField(max_length=10,choices=genderChoice)
    street=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    crime=models.ForeignKey(Crime,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Suspect(models.Model):
    genderChoice=[("M","Male"),("F","Females")]

    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    street=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=15)
    gender=models.CharField(max_length=10,choices=genderChoice)
    date_of_birth=models.DateField()
    crime=models.ForeignKey(Crime,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Victim(models.Model):
    genderChoice=[("M","Male"),("F","Females")]

    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    street=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=15)
    gender=models.CharField(max_length=10,choices=genderChoice)
    date_of_birth=models.DateField()
    crime=models.ForeignKey(Crime,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Evidence(models.Model):
    name=models.CharField(max_length=50)
    crime=models.ForeignKey(Crime,on_delete=models.CASCADE)
    date=models.DateField(default=timezone.now)
    description=models.TextField()

    def __str__(self):
        return self.name
