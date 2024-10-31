from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Station)
admin.site.register(PoliceModel) 
admin.site.register(Crime)
admin.site.register(Witness)
admin.site.register(Evidence)
admin.site.register(Suspect)
admin.site.register(Victim)