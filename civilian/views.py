from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
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

def login_civilian(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.user_type == 'Civilian':
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            error_message = 'Invalid Credentials!'
    return render(request, 'civilian_template/login.html', {'error':error_message})

@login_required
def logout_civilian(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return render(request, 'civilian_template/logout.html')

@login_required(login_url="login")
def home_civilian(request):
    return render(request, 'civilian_template/home.html')
