from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Slot, Booking

# Create your views here.

def home(request):
    return render(request, 'bookings/home.html')

@login_required
def book_slot(request):
    slots = Slot.objects.filter(is_available=True).order_by('start_time')
    if request.method == 'POST':
        slot_id = request.POST.get('slot')
        if slot_id:
            slot = Slot.objects.get(id=slot_id)
            # Create a booking (assuming you have a Booking model)
            Booking.objects.create(user=request.user, slot=slot)
            # Optionally mark slot as unavailable
            slot.is_available = False
            slot.save()
            return redirect('booking_confirmation')
    return render(request, 'bookings/book_slot.html', {'slots': slots})

def booking_confirmation(request):
    return render(request, 'bookings/booking_confirmation.html')

def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).select_related('slot').order_by('-booked_at')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        booking.is_cancelled = True  # Make sure your Booking model has this field
        booking.save()
        # Optionally, make the slot available again
        booking.slot.is_available = True
        booking.slot.save()
    except Booking.DoesNotExist:
        pass  # Optionally handle error or show a message
    return redirect('booking_list')

@login_required
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')

@login_required
@user_passes_test(lambda u: getattr(u, 'is_admin', False))
def admin_dashboard(request):
    return render(request, 'bookings/admin_dashboard.html')

@login_required
@user_passes_test(lambda u: getattr(u, 'is_admin', False))
def manage_slots(request):
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        if start_time and end_time:
            Slot.objects.create(start_time=start_time, end_time=end_time, is_available=True)
            return redirect('manage_slots')  # Redirect to avoid resubmission on refresh
    slots = Slot.objects.all().order_by('start_time')
    return render(request, 'bookings/manage_slots.html', {'slots': slots})

@login_required
@user_passes_test(lambda u: getattr(u, 'is_admin', False))
def edit_slot(request, slot_id):
    # Add your edit logic here
    return HttpResponse("Edit slot page (to be implemented)")

@login_required
@user_passes_test(lambda u: getattr(u, 'is_admin', False))
def delete_slot(request, slot_id):
    # Add your delete logic here
    return HttpResponse("Delete slot page (to be implemented)")

@login_required
@user_passes_test(lambda u: getattr(u, 'is_admin', False))
def admin_booking_list(request):
    bookings = Booking.objects.select_related('slot', 'user').order_by('-booked_at')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings, 'admin_view': True})

def error_404(request, exception):
    return render(request, 'bookings/404.html', status=404)
