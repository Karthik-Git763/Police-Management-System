from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth import login, authenticate, logout
from .form import RegisterForm, addCrime
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CivilianModel
from police.models import Crime, PoliceModel
# Create your views here.


# test for view
def is_civilian(user):
    return user.user_type == "Civilian"


# views


def register_civilian(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("civilianHome")
    else:
        form = RegisterForm()
    return render(request, "civilian_template/register.html", {"form": form})


def login_civilian(request):
    error_message = None
    next = request.GET.get("next", "civilianHome")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.user_type == "Civilian":
            login(request, user)
            next_url = (
                request.POST.get("next") or request.GET.get("next") or "civilianHome"
            )
            return redirect(next_url)
        else:
            error_message = "Invalid Credentials!"

    return render(
        request, "civilian_template/login.html", {"error": error_message, "next": next}
    )


@login_required(login_url="civilianLogin")
@user_passes_test(is_civilian, login_url="civilianLogin")
def logout_civilian(request):
    if request.method == "POST":
        logout(request)
        return redirect("civilianLogin")
    else:
        return render(request, "civilian_template/logout.html")


@login_required(login_url="civilianLogin")
@user_passes_test(is_civilian, login_url="civilianLogin")
def home_civilian(request):
    return render(request, "civilian_template/home.html")


@login_required
@user_passes_test(is_civilian, login_url="civilianLogin")
def add_Crime(request):
    if request.method == "POST":
        form = addCrime(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect("success")
    else:
        form = addCrime(request=request)

    return render(request, "civilian_template/addCrime.html", {"form": form})


@login_required
@user_passes_test(is_civilian, login_url="civilianLogin")
def add_Crime_success(request):
    return render(request, "civilian_template/success.html")


@login_required
@user_passes_test(is_civilian, login_url="civilianLogin")
def crime_submitted(request):
    user = request.user
    civilian = CivilianModel.objects.get(user=user)
    user_submited_crimes = Crime.objects.filter(submitted_by=civilian)
    return render(
        request,
        "civilian_template/submittedCrime.html",
        {"crimes": user_submited_crimes},
    )


@login_required
@user_passes_test(is_civilian, login_url="civilianLogin")
def submitted_crime_details(request, pk):
    user = request.user
    civilian = CivilianModel.objects.get(user=user)
    crime = Crime.objects.get(pk=pk)
    police = PoliceModel.objects.filter(current_crime=crime)
    if crime.submitted_by == civilian:
        return render(
            request,
            "civilian_template/submittedDetails.html",
            {"crime": crime, "policeOfficers": police},
        )
    else:
        return HttpResponse("You are not authorized")
