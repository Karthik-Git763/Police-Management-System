from django.contrib import admin
from .models import Station,PoliceModel,Crime
# Register your models here.

admin.site.register(Station)
admin.site.register(PoliceModel) 
admin.site.register(Crime)