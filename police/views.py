from django.shortcuts import render, redirect   
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Crime,PoliceModel
from django.db.models import Q

# Create your views here.

def is_police(user):
    return user.user_type=="Police"

def has_current_crime(user):
    police=PoliceModel.objects.get(user=user)
    return police.current_crime is not None

def login_police(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.user_type == 'Police':
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'policeHome'
            return redirect(next_url)
        else:
            error_message = 'Invalid Credentials!'
    return render(request, 'police_template/policeLogin.html', {'error':error_message})

@login_required
@user_passes_test(is_police,login_url="policeLogin")
def logout_police(request):
    if request.method == 'POST':
        logout(request)
        return redirect('policeLogin')
    else:
        return render(request, 'police_template/policeLogout.html')
    
@login_required(login_url="policeLogin")
@user_passes_test(is_police,login_url="policeLogin")
def home_police(request):
    return render(request, 'police_template/home.html')

@login_required(login_url="policeLogin")
@user_passes_test(is_police,login_url="policeLogin")
def view_pending_crimes(request):
    crimes=Crime.objects.filter(Q(status="Request Pending")| Q(status="Investigating"))
    return render(request,"police_template/pendingCrimes.html",{"crimes":crimes})

@login_required(login_url="policeLogin")
@user_passes_test(is_police,login_url="policeLogin")
def view_crime_details(request,pk): #later check if the current police has already selected one crime
    crime=Crime.objects.get(pk=pk)
    if request.method=="POST":
        police=PoliceModel.objects.get(user=request.user)
        if police.current_crime is not None:
            return render(request,"police_template/confirmCurrentCrimeChange.html",{"crime":crime})#change to render to different giving option to change and go to home
        police.current_crime=crime
        police.save()
        crime.status="Investigating"
        crime.save()
        return redirect("policeHome")
    else:
        #user=request.user
        # police=PoliceModel.objects.get(user=user)
        # if police.current_crime is not None:
        #     return render(request,)
        return render(request,"police_template/crimeDetails.html",{"crime":crime})

@login_required(login_url="policeLogin")
@user_passes_test(is_police,login_url="policeLogin")
@user_passes_test(has_current_crime,login_url="pendingCrimes")
def cancel_current_crime(request):
    user=request.user
    police=PoliceModel.objects.get(user=user)
    crime=police.current_crime
    if request.method=="POST":
        police.current_crime=None
        #to do
        #if no one else is doing that crime change to pending else keep it as investivating 
        crime.status=request.POST.get("status")#add status choice in form
        #check later if needed
        # if crime.status=="Similiar Repoted"
        #      change for all who have selected this a crime
        police.save()
        crime.save()
        return redirect("policeHome")
    else:
        return render(request,"police_template/cancelCrime.html",{"crime":crime})
    
