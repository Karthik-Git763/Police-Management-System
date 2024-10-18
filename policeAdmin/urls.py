from django.urls import path
from .views import add_police,add_station,add_police_admin,admin_login,admin_logout,admin_home
urlpatterns = [
    path("addPolice",add_police,name="addPolice"),
    path("addStation",add_station,name="addStation"),
    path("addPoliceAdmin",add_police_admin,name="addPoliceAdmin"),
    path("adminLogin",admin_login,name="adminLogin"),
    path("adminLogout",admin_logout,name="adminLogout"),
    path("adminHome",admin_home,name="adminHome"),
]