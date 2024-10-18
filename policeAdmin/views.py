from django.shortcuts import render,redirect
from .forms import AddPoliceForm,AddStationForm,AddPoliceAdminForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def add_police(request):# check later if working after admin login
    if request.method=="POST":
        form=AddPoliceForm(request.POST,request=request)
        if form.is_valid():
            form.save()
            return redirect("adminHome")#temp change later
    else:
        form=AddPoliceForm(request=request)
    return render(request,"admin_templates/addPolice.html",{"form":form})

def add_station(request):
    if request.method=="POST":
        form=AddStationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("adminHome")
    else:
        form=AddStationForm()
    return render(request,"admin_templates/addStation.html",{"form":form})


def add_police_admin(request):
    if request.method=="POST":
        form=AddPoliceAdminForm(request.POST)
        if form.is_valid():
            user=form.save()
            return redirect("adminHome")
    else:
        form=AddPoliceAdminForm()
    return render(request,"admin_templates/addPoliceAdmin.html",{"form":form})


def admin_login(request):
    error_message=None
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None and user.user_type=="Admin":
            login(request,user)
            return redirect("adminHome")
        else:
            error_message="Invalid credentials or user not admin"
    return render(request,"admin_templates/adminLogin.html",{"errorMsg":error_message})

#login as sdmin required
def admin_logout(request):
    if request.method=="POST":
        logout(request)
        return redirect("adminLogin")
    else:
        return render(request,"admin_templates/adminLogout.html")
    
def admin_home(request):
    return render(request,"admin_templates/home.html")
