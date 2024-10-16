from django.contrib import admin
from .models import CivilianModel,CustomUser
# Register your models here.
admin.site.register(CivilianModel)
admin.site.register(CustomUser)
