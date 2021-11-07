from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import login as auth_login, logout as auth_logout
from user_side.models import *
from .forms import *

def admin_dashboard(request):
    if request.method == 'GET':
        if request.session.has_key('admin'):
            student = Student.objects.all()
            return render(request, 'admin_panel/admin_dashboard.html', {"student": student})
        else:
            return redirect('admin_login')
    return render(request, 'admin_panel/admin_dashboard.html')

def admin_login(request):
    if request.method == 'GET':
        if request.session.has_key('admin'):
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_panel/admin_login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        auth_user = auth.authenticate(username=username, password=password)
        if auth_user is not None and auth_user.is_superuser == True:
            request.session['admin'] = True
            return redirect('admin_dashboard')
        else:
            invalid_error = "Invalid creditials ! !"
            return render(request, 'admin_panel/admin_login.html', {'error':invalid_error})

def admin_logout(request):
    del request.session['admin']
    return redirect('admin_login')

def edit_student(request, id):
    if request.method == 'GET':
        student = Student.objects.get(user=id)
        form = StudentForm(instance=student)
        return render(request, 'admin_panel/edit_student.html', {'form': form, "student": student})
    if request.method == 'POST':
        student = Student.objects.get(user=id)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_panel/edit_student.html', {'form': form})