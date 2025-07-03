from django.shortcuts import render, redirect

def user_register(request):
    return render(request, 'accounts/user_register.html')

def user_login(request):
    return render(request, 'accounts/user_login.html')

def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')

def admin_register(request):
    return render(request, 'accounts/admin_register.html')

def admin_login(request):
    return render(request, 'accounts/admin_login.html')
