from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, auth
from .models import *

def dashboard(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            print("---user1---", request.user)
            account = Account.objects.get(user=request.user)
            return render(request, 'dashboard.html', {"account": account})
        else:
            return redirect('login')
    return render(request, 'dashboard.html')
    
def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        auth_user = auth.authenticate(username=user, password=password)
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

def update_personal_details(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            print("---user1---", request.user)
            account = Account.objects.get(user=request.user)
            day = account.dob.strftime('%d')
            month = account.dob.strftime('%m')
            year = account.dob.strftime('%Y')
            context = {
                'account': account,
                'day': day,
                'month': month,
                'year': year,
            }
            return render(request, 'update_personal_details.html', context)
        else:
            return redirect('login')
            
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')

        user = User.objects.filter(username=username)

        if user.count() > 1:
            return render(request, 'update_personal_details.html', {'error': "Username already exists!"})
        else:
            try:
                user = User.objects.get(username=username)
                user.username = username
                user.email = email
                user.save()
                account = Account.objects.get(user=user)
                account.phone = phone
                account.dob = dob
                account.save()
                return redirect('dashboard')
            except:
                return render(request, 'update_personal_details.html', {'error': "Something went wrong!"})
