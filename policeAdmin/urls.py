from django.urls import path
from .views import add_police,add_station,add_police_admin
urlpatterns = [
    path("addPolice",add_police,name="addPolice"),
    path("addStation",add_station,name="addStation"),
    path("addPoliceAdmin",add_police_admin,name="addPoliceAdmin"),
]