from django.urls import path
from . import views

urlpatterns = [
    path('Home/', views.home_police, name='policeHome'),
    path('login/', views.login_police, name='policeLogin'),
    path('logout/', views.logout_police, name='policeLogout'),
]