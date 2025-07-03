from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Slot, Booking

User = get_user_model()

class BookingSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin = User.objects.create_user(username='admin', password='adminpass', is_admin=True)
        self.slot = Slot.objects.create(start_time='2025-07-03T10:00', end_time='2025-07-03T11:00', is_available=True)

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        response = self.client.post(reverse('user_register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration

    def test_user_login(self):
        response = self.client.post(reverse('user_login'), {
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_book_slot(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('book_slot'), {
            'slot': self.slot.id,
        })
        self.assertRedirects(response, reverse('booking_confirmation'))
        self.slot.refresh_from_db()
        self.assertFalse(self.slot.is_available)
        self.assertTrue(Booking.objects.filter(user=self.user, slot=self.slot).exists())

    def test_booking_list(self):
        Booking.objects.create(user=self.user, slot=self.slot)
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('booking_list'))
        self.assertContains(response, 'My Bookings')

    def test_admin_login_and_dashboard(self):
        response = self.client.post(reverse('admin_login'), {
            'username': 'admin',
            'password': 'adminpass',
        })
        self.assertEqual(response.status_code, 302)
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_manage_slots(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('manage_slots'))
        self.assertEqual(response.status_code, 200)

    def test_cancel_booking(self):
        self.client.login(username='testuser', password='testpass')
        booking = Booking.objects.create(user=self.user, slot=self.slot)
        response = self.client.get(reverse('cancel_booking', args=[booking.id]))
        booking.refresh_from_db()
        self.assertTrue(booking.is_cancelled)
        self.assertRedirects(response, reverse('booking_list'))

    def test_admin_booking_list(self):
        Booking.objects.create(user=self.user, slot=self.slot)
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('admin_booking_list'))
        self.assertContains(response, 'testuser')
