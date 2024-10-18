from django.shortcuts import render,redirect
from .forms import AddPoliceForm,AddStationForm,AddPoliceAdminForm
from django.contrib.auth import login, authenticate, logout#temp
# Create your views here.

def add_police(request):# check later if working after admin login
    if request.method=="POST":
        form=AddPoliceForm(request.POST,request=request)
        if form.is_valid():
            form.save()
            return redirect("home")#temp change later
    else:
        form=AddPoliceForm()
    return render(request,"admin_templates/addPolice.html",{"form":form})

def add_station(request):
    if request.method=="POST":
        form=AddStationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")# temp change later
    else:
        form=AddStationForm()
    return render(request,"admin_templates/addStation.html",{"form":form})


def add_police_admin(request):
    print("here")
    if request.method=="POST":
        form=AddPoliceAdminForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)# remove later

            return redirect("home")#change later
    else:
        form=AddPoliceAdminForm()
    return render(request,"admin_templates/addPoliceAdmin.html",{"form":form})