from django.shortcuts import render, redirect
from django.contrib.auth import login
from .form import RegisterForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def register_civilian(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'civilian_template/register.html', {'form': form})

# @login_required
def home_civilian(request):
    return render(request, 'civilian_template/home.html')
