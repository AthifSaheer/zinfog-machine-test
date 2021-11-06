from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, auth
from .models import *

def dashboard(request):
    return render(request, 'dashboard.html')
    
def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        auth_user = auth.authenticate(username=user, password=password)
        print("----------", auth_user)
        if auth_user is not None:
            usr = User.objects.get(username=user)
            auth_login(request, usr)
            # iflogout usr.is_superuser == True:
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': "Invalid credentials"})
                
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        password = request.POST.get('password')

        if User.objects.filter(username=username):
            return render(request, 'register.html', {'error': "Username already exists!"})
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                Account.objects.create(user=user, phone=phone, dob=dob)
                return redirect('dashboard')
            except:
                return render(request, 'register.html', {'error': "Something went wrong!"})

    return render(request, 'register.html')

def logout(request):
    auth_logout(request)
    return redirect('login')