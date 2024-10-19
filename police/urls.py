from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_police, name='policeHome'),
    path('login/', views.login_police, name='policeLogin'),
    path('logout/', views.logout_police, name='policeLogout'),
    path('selectCrime/',views.view_pending_crimes,name="pendingCrimes"),
    path("crimeDetail/<int:pk>",views.view_crime_details,name="crime"),
    path("cancelCrime/",views.cancel_current_crime,name="cancelCrime"),
]