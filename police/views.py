from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Crime,PoliceModel
from .form import WitnessForm
from django.db.models import Q
from django.contrib import messages
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
    crimes=Crime.objects.filter(Q(status="Request Pending")| Q(status="Investigating"))
    return render(request,"police_template/pendingCrimes.html",{"crimes":crimes})

@login_required(login_url="policeLogin")
@user_passes_test(is_police,login_url="policeLogin")
def view_crime_details(request,pk): #later check if the current police has already selected one crime
    crime=Crime.objects.get(pk=pk)
    if request.method=="POST":
        police=PoliceModel.objects.get(user=request.user)
        if police.current_crime is not None:
            return render(request,"police_template/confirmCurrentCrimeChange.html",{"crime":crime})
        police.current_crime=crime
        police.save()
        crime.status="Investigating"
        crime.save()
        messages.success(request, f'The crime {crime} has been selected ')
        return redirect("policeHome")
    else:
        #user=request.user
        # police=PoliceModel.objects.get(user=user)
        # if police.current_crime is not None:
        #     return render(request,)
        return render(request,"police_template/crimeDetails.html",{"crime":crime})

@login_required(login_url="policeLogin")
@user_passes_test(is_police,login_url="policeLogin")
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
        messages.success(request, 'Current crime under investigation has been unselected')
        return redirect("policeHome")
    else:
        if police.current_crime is None:
            messages.error(request ,"Select a crime first ")
            return redirect("policeHome")
        return render(request,"police_template/cancelCrime.html",{"crime":crime})


@login_required(login_url="policeLogin")
@user_passes_test(is_police,login_url="policeLogin")
def add_witness(request):

    police=PoliceModel.objects.get(user=request.user)
    crime=police.current_crime
    if crime is None:
        messages.error(request, "No crime selected for investigation. Please select a crime first.")
        return redirect('policeHome')  # Redirect if no crime is selected
    if request.method == 'POST':
        form = WitnessForm(request.POST)
        if form.is_valid():
            witness = form.save(commit=False)
            witness.crime = crime  # Link the witness to the selected crime
            witness.added_by=police
            witness.save()
            messages.success(request, 'Witness added successfully.')
            return redirect('policeHome')  # Redirect to the police home after submission
    else:
        form = WitnessForm()

    return render(request, 'police_template/addWitness.html', {'form': form, 'crime': crime})
