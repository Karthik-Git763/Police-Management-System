from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_civilian, name='home'),
    path('register/', views.register_civilian, name='register'),
]