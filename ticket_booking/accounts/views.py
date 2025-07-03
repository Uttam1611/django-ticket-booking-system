from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        photo = request.FILES.get('photo')
        if password1 == password2:
            User = get_user_model()
            user = User.objects.create_user(username=username, email=email, password=password1, photo=photo)
            return redirect('user_login')
        else:
            return render(request, 'accounts/user_register.html', {
                'form': {},
                'error': 'Passwords do not match'
            })
    return render(request, 'accounts/user_register.html', {'form': {}})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_dashboard')  # or any page you want
        else:
            return render(request, 'accounts/user_login.html', {
                'form': {},  # If you use a form, pass it here
                'error': 'Invalid username or password'
            })
    return render(request, 'accounts/user_login.html', {'form': {}})

@login_required
def user_dashboard(request):
    if getattr(request.user, 'is_admin', False):
        raise PermissionDenied
    return render(request, 'accounts/user_dashboard.html')

def admin_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            User = get_user_model()
            user = User.objects.create_user(username=username, email=email, password=password1, is_admin=True)
            return redirect('admin_login')
        else:
            return render(request, 'accounts/admin_register.html', {
                'form': {},
                'error': 'Passwords do not match'
            })
    return render(request, 'accounts/admin_register.html', {'form': {}})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Username: {username}, Password: {password}")  # Debug
        user = authenticate(request, username=username, password=password)
        print(f"User: {user}")  # Debug
        if user is not None and getattr(user, 'is_admin', False):
            print("Admin login successful")  # Debug
            login(request, user)
            return redirect('admin_dashboard')
        else:
            print("Admin login failed")  # Debug
            return render(request, 'accounts/admin_login.html', {
                'form': {},
                'error': 'Invalid admin credentials'
            })
    return render(request, 'accounts/admin_login.html', {'form': {}})

def user_logout(request):
    logout(request)
    return redirect('user_login')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required
@user_passes_test(lambda u: getattr(u, 'is_admin', False))
def admin_dashboard(request):
    return render(request, 'bookings/admin_dashboard.html')
