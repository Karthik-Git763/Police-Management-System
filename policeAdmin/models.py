from django.db import models
from civilian.models import CustomUser

# Create your models here.
class AdminModel(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

