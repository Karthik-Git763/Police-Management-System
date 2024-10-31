from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_civilian, name='civilianHome'),
    path('register/', views.register_civilian, name='civilianRegister'),
    path('login/', views.login_civilian, name='civilianLogin'),
    path('logout/', views.logout_civilian, name='civilianLogout'),
    path('addCrime/', views.add_Crime, name='addCrime'),
    path('addCrime/success/', views.add_Crime_success, name='success')
]