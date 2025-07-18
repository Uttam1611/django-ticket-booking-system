from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_slot, name='book_slot'),
    path('confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('list/', views.booking_list, name='booking_list'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-slots/', views.manage_slots, name='manage_slots'),
    path('edit-slot/<int:slot_id>/', views.edit_slot, name='edit_slot'),
    path('delete-slot/<int:slot_id>/', views.delete_slot, name='delete_slot'),
    path('admin-bookings/', views.admin_booking_list, name='admin_booking_list'),
]