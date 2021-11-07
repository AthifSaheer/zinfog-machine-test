from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import login as auth_login, logout as auth_logout
from user_side.models import *


def admin_dashboard(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            print("---user1---", request.user)
            account = Account.objects.get(user=request.user)
            return render(request, 'admin/dashboard.html', {"account": account})
        else:
            return redirect('login')
    return render(request, 'admin/dashboard.html')
    
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
            return render(request, 'user/login.html', {'error': "Invalid credentials"})
                
    return render(request, 'user/login.html')


def admin_login(request):
    if request.method == 'GET':
        if request.session.has_key('admin'):
            return redirect('admin_dashboard')
        else:
            return render(request, 'user/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        auth_user = auth.authenticate(username=username, password=password)
        if auth_user is not None and auth_user.is_superuser == True:
            request.session['admin'] = True
            return redirect('admin_dashboard')
        else:
            invalid_error = "Invalid creditials ! !"
            return render(request, 'user/login.html', {'error':invalid_error})

def admin_logout(request):
    del request.session['admin']
    return redirect('login')
