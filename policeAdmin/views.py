from django.shortcuts import render,redirect
from .forms import AddPoliceForm,AddStationForm,AddPoliceAdminForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate,login,logout
# Create your views here.
#test fro views
def is_admin(user):
    return user.user_type=="Admin"



#views 
@login_required(login_url="adminLogin")
@user_passes_test(is_admin,login_url="adminLogin")
def add_police(request):# check later if working after admin login
    if request.method=="POST":
        form=AddPoliceForm(request.POST,request=request)
        if form.is_valid():
            form.save()
            return redirect("admin_home")
    else:
        form=AddPoliceForm(request=request)
    return render(request,"admin_templates/addPolice.html",{"form":form})

@login_required(login_url="adminLogin")
@user_passes_test(is_admin,login_url="adminLogin")
def add_station(request):
    if request.method=="POST":
        form=AddStationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_home")
    else:
        form=AddStationForm()
    return render(request,"admin_templates/addStation.html",{"form":form})


@login_required(login_url="adminLogin")
@user_passes_test(is_admin,login_url="adminLogin")
def add_police_admin(request):
    if request.method=="POST":
        form=AddPoliceAdminForm(request.POST)
        if form.is_valid():
            user=form.save()
            return redirect("admin_home")
    else:
        form=AddPoliceAdminForm()
    return render(request,"admin_templates/addPoliceAdmin.html",{"form":form})


def admin_login(request):
    error_message=None
    next = request.GET.get('next',"adminHome")
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None and user.user_type=="Admin":
            login(request,user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'adminHome'
            return redirect(next_url)
        else:
            error_message="Invalid credentials or user not admin"
    return render(request,"admin_templates/adminLogin.html",{"errorMsg":error_message,"next":next})

@login_required(login_url="adminLogin")
@user_passes_test(is_admin,login_url="adminLogin")
def admin_logout(request):
    if request.method=="POST":
        logout(request)
        return redirect("adminLogin")
    else:
        return render(request,"admin_templates/adminLogout.html")
    
@login_required(login_url="adminLogin")
@user_passes_test(is_admin,login_url="adminLogin")
def admin_home(request):
    return render(request,"admin_templates/home.html")
