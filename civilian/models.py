from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    userTypeChoice = [
        ("Civilian", "Civilian"),
        ("Admin", "Admin"),
        ("Police", "Police"),
    ]
    user_type = models.CharField(max_length=15, choices=userTypeChoice)


class CivilianModel(models.Model):
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
