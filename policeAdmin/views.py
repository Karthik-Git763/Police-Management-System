from django.shortcuts import render,redirect
from .forms import AddPolice
# Create your views here.

def add_police(request):
    if request.method=="POST":
        form=AddPolice(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form=AddPolice()
    return render("admin_templates/addPolice.html",{"form":form})