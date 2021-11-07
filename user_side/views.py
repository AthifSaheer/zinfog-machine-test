from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.files.images import get_image_dimensions
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from datetime import datetime
from .models import *
from .forms import *

def dashboard(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                account = Student.objects.get(user=request.user)
                return render(request, 'user/dashboard.html', {"account": account})
            except Student.DoesNotExist:
                return redirect('login')
        else:
            return redirect('login')
    return render(request, 'user/dashboard.html')
    
def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        auth_user = auth.authenticate(username=user, password=password)
        if auth_user is not None:
            usr = User.objects.get(username=user)
            auth_login(request, usr)
            return redirect('dashboard')
        else:
            return render(request, 'user/login.html', {'error': "Invalid credentials"})
                
    return render(request, 'user/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        password = request.POST.get('password')

        if User.objects.filter(username=username):
            return render(request, 'user/register.html', {'error': "Username already exists!"})
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                Student.objects.create(user=user, phone=phone, dob=dob)
                usr = User.objects.get(username=user)
                auth_login(request, usr)
                return redirect('dashboard')
            except:
                return render(request, 'user/register.html', {'error': "Something went wrong!"})

    return render(request, 'user/register.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

def update_personal_details(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            print("---user1---", request.user)
            account = Student.objects.get(user=request.user)
            day = account.dob.strftime('%d')
            month = account.dob.strftime('%m')
            year = account.dob.strftime('%Y')
            context = {
                'account': account,
                'day': day,
                'month': month,
                'year': year,
            }
            return render(request, 'user/update_personal_details.html', context)
        else:
            return redirect('login')
            
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')

        user = User.objects.filter(username=username)

        if user.count() > 1:
            return render(request, 'user/update_personal_details.html', {'error': "Username already exists!"})
        else:
            try:
                user = User.objects.get(username=request.user.username)
                user.username = username
                user.email = email
                user.save()
                account = Student.objects.get(user=user)
                account.phone = phone
                account.dob = dob
                account.save()
                return redirect('dashboard')
            except:
                return render(request, 'user/update_personal_details.html', {'error': "Something went wrong!"})

def profile(request, id):
    if request.method == 'GET':
        form = ProfileImageForm()
        try:
            profile = ProfileImage.objects.get(user=id)
        except ProfileImage.DoesNotExist:
            profile = None
        try:
            student = Student.objects.get(user=id)
            dob_year = student.dob.strftime('%Y')
            current_year = datetime.now().year
            age = int(current_year) - int(dob_year)
            context = {
                'student': student,
                'profile': profile,
                "age": age,
                'form': form,
            }
            return render(request, 'user/profile.html', context)
        except:
            print("=====age---")
            return render(request, 'user/profile.html')

    if request.method == 'POST':
        data = request.POST.copy()
        data['user'] = User.objects.get(id=id)
        form = ProfileImageForm(data, request.FILES)
        if form.is_valid():
            form.save()
        
        prf_img = ProfileImage.objects.get(user=id)
        w, h = get_image_dimensions(prf_img.image)
        print("Image---wh--", w, h)

        if w != 300:
            return render(request, 'user/profile.html', {'error': "Image should be 300x356!"})
        if h != 356:
            return render(request, 'user/profile.html', {'error': "Image should be 300x356!"})
        return render(request, 'user/profile.html')
