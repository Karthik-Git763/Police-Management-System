from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Crime, PoliceModel, Evidence
from .form import *
from .form import WitnessForm, EvidenceForm, CriminalForm
from django.db.models import Q
from django.contrib import messages
# Create your views here.


def is_police(user):
    return user.user_type == "Police"


def login_police(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.user_type == "Police":
            login(request, user)
            next_url = (
                request.POST.get("next") or request.GET.get("next") or "policeHome"
            )
            return redirect(next_url)
        else:
            error_message = "Invalid Credentials!"
    return render(request, "police_template/policeLogin.html", {"error": error_message})


@login_required
@user_passes_test(is_police, login_url="policeLogin")
def logout_police(request):
    if request.method == "POST":
        logout(request)
        return redirect("policeLogin")
    else:
        return render(request, "police_template/policeLogout.html")


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def home_police(request):
    police = PoliceModel.objects.get(user=request.user)
    current_crime = police.current_crime
    return render(
        request, "police_template/home.html", {"current_crime": current_crime}
    )


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def view_pending_crimes(request):
    crimes = Crime.objects.filter(
        Q(status="Request Pending") | Q(status="Investigating")
    )
    return render(request, "police_template/pendingCrimes.html", {"crimes": crimes})


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def view_crime_details(
    request, pk
):  # later check if the current police has already selected one crime
    crime = Crime.objects.get(pk=pk)
    if request.method == "POST":
        police = PoliceModel.objects.get(user=request.user)
        if police.current_crime is not None:
            return render(
                request,
                "police_template/confirmCurrentCrimeChange.html",
                {"crime": crime},
            )
        police.current_crime = crime
        police.save()
        crime.status = "Investigating"
        crime.save()
        messages.success(request, f"The crime {crime} has been selected ")
        return redirect("policeHome")
    else:
        police = PoliceModel.objects.filter(current_crime=crime)
        witnesses = Witness.objects.filter(crime=crime)
        victims = Victim.objects.filter(crime=crime)
        suspects = Suspect.objects.filter(crime=crime)
        evidences = Evidence.objects.filter(crime=crime)

        return render(
            request,
            "police_template/crimeDetails.html",
            {
                "crime": crime,
                "police": police,
                "witnesses": witnesses,
                "victims": victims,
                "suspects": suspects,
                "evidences": evidences,
            },
        )


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def cancel_current_crime(request):
    user = request.user
    police = PoliceModel.objects.get(user=user)
    crime = police.current_crime
    if request.method == "POST":
        police.current_crime = None
        other_crimes = (
            PoliceModel.objects.exclude(id=police.id)
            .filter(current_crime=crime)
            .exists()
        )  # Check if an officer is working in a crime or not in others perspective also
        if not other_crimes:
            crime.status = "Request Pending"
        else:
            crime.status = "Investigating"

        police.save()
        crime.save()
        messages.success(
            request, "Current crime under investigation has been unselected"
        )
        return redirect("policeHome")
    else:
        if police.current_crime is None:
            messages.error(request, "Select a crime first ")
            return redirect("policeHome")
        return render(request, "police_template/cancelCrime.html", {"crime": crime})


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def add_witness(request):
    police = PoliceModel.objects.get(user=request.user)
    crime = police.current_crime
    if crime is None:
        messages.error(
            request, "No crime selected for investigation. Please select a crime first."
        )
        return redirect("policeHome")  # Redirect if no crime is selected
    if request.method == "POST":
        form = WitnessForm(request.POST)
        if form.is_valid():
            witness = form.save(commit=False)
            witness.crime = crime  # Link the witness to the selected crime
            witness.added_by = police
            witness.save()
            messages.success(request, "Witness added successfully.")
            return redirect(
                "policeHome"
            )  # Redirect to the police home after submission
    else:
        form = WitnessForm()

    return render(
        request, "police_template/addWitness.html", {"form": form, "crime": crime}
    )


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def add_evidence(request):
    police = PoliceModel.objects.get(user=request.user)
    crime = police.current_crime
    if crime is None:
        messages.error(
            request, "No crime selected for investigation. Please select a crime first."
        )
        return redirect("policeHome")

    if request.method == "POST":
        form = EvidenceForm(request.POST, request.FILES)
        if form.is_valid():
            evidence = form.save(commit=False)
            evidence.crime = crime
            evidence.added_by = police
            evidence.save()
            messages.success(request, "Evidence added successfully!")
            return redirect("policeHome")
    else:
        form = EvidenceForm()

    return render(
        request, "police_template/addEvidence.html", {"form": form, "crime": crime}
    )


def evidence_list(request):
    evidences = Evidence.objects.all()
    return render(
        request, "police_template/evidence_list.html", {"evidences": evidences}
    )


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def add_suspect(request):
    police = PoliceModel.objects.get(user=request.user)
    crime = police.current_crime
    if crime is None:
        messages.error(
            request, "No crime selected for investigation. Please select a crime first."
        )
        return redirect("policeHome")

    if request.method == "POST":
        form = SuspectForm(request.POST)
        if form.is_valid():
            suspect = form.save(commit=False)
            suspect.crime = crime
            suspect.added_by = police
            suspect.save()
            messages.success(request, "Suspect added successfully!")
            return redirect("policeHome")
    else:
        form = SuspectForm()

    return render(
        request, "police_template/addSuspect.html", {"form": form, "crime": crime}
    )


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def add_victim(request):
    police = PoliceModel.objects.get(user=request.user)
    crime = police.current_crime
    if crime is None:
        messages.error(
            request, "No crime selected for investigation. Please select a crime first."
        )
        return redirect("policeHome")

    if request.method == "POST":
        form = VictimForm(request.POST)
        if form.is_valid():
            victim = form.save(commit=False)
            victim.crime = crime
            victim.added_by = police
            victim.save()
            messages.success(request, "Victim added successfully!")
            return redirect("policeHome")
    else:
        form = VictimForm()

    return render(
        request, "police_template/addVictim.html", {"form": form, "crime": crime}
    )


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def add_criminal(request):
    if request.method == "POST":
        form = CriminalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Criminal added successfully")
            return redirect("policeHome")
    else:
        form = CriminalForm()
    return render(request, "police_template/addCriminal.html", {"form": form})


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def add_criminal_to_current_crime(request):
    police = PoliceModel.objects.get(user=request.user)
    crime = police.current_crime
    if crime is None:
        messages.error(request, "Select a crime first")
        redirect("policeHome")
    if request.method == "POST":
        form = CriminalToCrimeForm(request.POST)
        if form.is_valid():
            criminal = form.cleaned_data["criminal"]
            crime.criminal_set.add(criminal)
            messages.success(
                request, f"Criminal successfully add to crime {str(crime)}"
            )
            return redirect("policeHome")
        messages.error(request, "Form was invalid")
        return redirect("policeHome")
    else:
        form = CriminalToCrimeForm()
    return render(
        request, "police_template/criminalToCrime.html", {"crime": crime, "form": form}
    )


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def view_criminals(request):
    all_criminals = Criminal.objects.all()
    return render(
        request, "police_template/viewCriminals.html", {"criminals": all_criminals}
    )


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def criminal_details(request, id):
    criminal = Criminal.objects.get(id=id)
    return render(
        request, "police_template/criminalDetails.html", {"criminal": criminal}
    )


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def witness_detail(request, pk):
    witness = Witness.objects.get(pk=pk)
    return render(request, "police_template/witnessDetails.html", {"witness": witness})


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def victim_detail(request, pk):
    victim = Victim.objects.get(pk=pk)
    return render(request, "police_template/victimDetails.html", {"victim": victim})


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def suspect_detail(request, pk):
    suspect = Suspect.objects.get(pk=pk)
    return render(request, "police_template/suspectDetails.html", {"suspect": suspect})


@login_required(login_url="policeLogin")
@user_passes_test(is_police, login_url="policeLogin")
def evidence_detail(request, pk):
    evidence = Evidence.objects.get(pk=pk)
    return render(
        request, "police_template/evidenceDetails.html", {"evidence": evidence}
    )


# to do add update option to all_criminals
class UpdateWitness(LoginRequiredMixin, UpdateView):
    template_name = "police_template/updateWitness.html"
    model = Witness
    fields = {
        "first_name",
        "last_name",
        "statement",
        "phone_number",
        "gender",
        "street",
        "city",
        "state",
    }

    def dispatch(self, request, *args, **kwargs):
        currentWitness = self.get_object()
        police = PoliceModel.objects.get(user=self.request.user)
        witness = Witness.objects.filter(
            crime=police.current_crime, id=currentWitness.id
        )
        if not witness.exists():
            messages.error(
                request,
                "You can only change witness of crime you are currently investigating",
            )
            return redirect(reverse("policeHome"))
        return super().dispatch(request, *args, **kwargs)


class UpdateVictim(LoginRequiredMixin, UpdateView):
    template_name = "police_template/updateVictim.html"
    model = Victim
    fields = {
        "first_name",
        "last_name",
        "date_of_birth",
        "phone_number",
        "gender",
        "street",
        "city",
        "state",
    }

    def dispatch(self, request, *args, **kwargs):
        currentVictim = self.get_object()
        police = PoliceModel.objects.get(user=self.request.user)
        victim = Victim.objects.filter(crime=police.current_crime, id=currentVictim.id)
        if not victim.exists():
            messages.error(
                request,
                "You can only change victim of crime you are currently investigating",
            )
            return redirect(reverse("policeHome"))
        return super().dispatch(request, *args, **kwargs)


class UpdateEvidence(LoginRequiredMixin, UpdateView):
    template_name = "police_template/updateEvidence.html"
    model = Evidence
    fields = {
        "name",
        "description",
    }

    def dispatch(self, request, *args, **kwargs):
        currentEvidence = self.get_object()
        police = PoliceModel.objects.get(user=self.request.user)
        evidence = Evidence.objects.filter(
            crime=police.current_crime, id=currentEvidence.id
        )
        if not evidence.exists():
            messages.error(
                request,
                "You can only change evidence of crime you are currently investigating",
            )
            return redirect(reverse("policeHome"))
        return super().dispatch(request, *args, **kwargs)


class UpdateSuspect(LoginRequiredMixin, UpdateView):
    template_name = "police_template/updateSuspect.html"
    model = Suspect
    fields = {
        "first_name",
        "last_name",
        "date_of_birth",
        "phone_number",
        "gender",
        "street",
        "city",
        "state",
    }

    def dispatch(self, request, *args, **kwargs):
        currentSuspect = self.get_object()
        police = PoliceModel.objects.get(user=self.request.user)
        suspect = Suspect.objects.filter(
            crime=police.current_crime, id=currentSuspect.id
        )
        if not suspect.exists():
            messages.error(
                request,
                "You can only change Suspect of crime you are currently investigating",
            )
            return redirect(reverse("policeHome"))
        return super().dispatch(request, *args, **kwargs)


def completeCrime(request):
    if request.method == "POST":
        user = request.user
        police = PoliceModel.objects.get(user=user)
        crime = police.current_crime
        crime.status = "Completed"
        crime.save()
        PoliceModel.objects.filter(current_crime=crime).update(current_crime=None)
        messages.success(request, "Crime has been successfully updated to completed")
        return redirect("policeHome")
    else:
        return render(request, "police_template/completeCrime.html")
