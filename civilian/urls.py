from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_civilian, name='home'),
    path('register/', views.register_civilian, name='register'),
    path('login/', views.login_civilian, name='login'),
    path('logout/', views.logout_civilian, name='logout'),
    path('addCrime/', views.add_Crime, name='addCrime'),
    path('addCrime/success/', views.add_Crime_success, name='success')
]