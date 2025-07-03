from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'bookings/home.html')

def book_slot(request):
    return render(request, 'bookings/book_slot.html')

def booking_confirmation(request):
    return render(request, 'bookings/booking_confirmation.html')

def booking_list(request):
    return render(request, 'bookings/booking_list.html')

def cancel_booking(request, booking_id):
    # Logic to cancel booking
    return redirect('booking_list')

def admin_dashboard(request):
    return render(request, 'bookings/admin_dashboard.html')

def manage_slots(request):
    return render(request, 'bookings/manage_slots.html')

def error_404(request, exception):
    return render(request, 'bookings/404.html', status=404)
