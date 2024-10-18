from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

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
def logout_police(request):
    if request.method == 'POST':
        logout(request)
        return redirect('policeLogin')
    else:
        return render(request, 'police_template/policeLogout.html')
    
@login_required(login_url="policeLogin")
def home_police(request):
    return render(request, 'police_template/home.html')