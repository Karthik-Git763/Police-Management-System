from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Crime,PoliceModel
# Create your views here.

def is_police(user):
    return user.user_type=="Police"

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
    crimes=Crime.objects.filter(status="Request Pending")
    return render(request,"police_template/pendingCrimes.html",{"crimes":crimes})

@login_required(login_url="policeLogin")
@user_passes_test(is_police,login_url="policeLogin")
def view_crime_details(request,pk): #later check if the current police has already selected one crime
    crime=Crime.objects.get(pk=pk)
    if request.method=="POST":
        police=PoliceModel.objects.get(user=request.user)
        police.current_crime=crime
        police.save()
        crime.status="Investigating"
        crime.save()
        return redirect("policeHome")
    else:
        return render(request,"police_template/crimeDetails.html",{"crime":crime})
